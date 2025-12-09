import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import plotly.express as px

from utils.network_utils import get_multi_iface_stats
from utils.anomaly import detect_anomalies
from utils.ui_utils import show_quote
from utils.constants import PLOTLY_CONFIG
import psutil

def real_time_monitor():
    st.title("📡 Real-Time WiFi Monitor")

    # discover interfaces
    all_ifaces = list(psutil.net_io_counters(pernic=True).keys())

    # heuristics to pick likely wireless interfaces across platforms
    default_ifaces = [
        iface for iface in all_ifaces
        if any(k in iface.lower() for k in ("wi-fi", "wifi", "wlan", "wl", "wlp"))
    ]
    if not default_ifaces and all_ifaces:
        default_ifaces = [all_ifaces[0]]

    selected_ifaces = st.multiselect(
        "Select Interfaces", all_ifaces,
        default=default_ifaces
    )

    if not selected_ifaces:
        st.warning("Please select at least one interface")
        show_quote()
        return

    # refresh every 5 seconds
    st_autorefresh(interval=5000, key="auto_refresh")

    current_df = get_multi_iface_stats(selected_ifaces)

    # append only new rows (current_df contains per-interval deltas)
    if not current_df.empty:
        # ensure history exists
        if "history" not in st.session_state:
            st.session_state.history = pd.DataFrame(
                columns=[
                    "timestamp", "interface", "ip_address", "location",
                    "bytes_sent", "bytes_recv", "cum_bytes_sent", "cum_bytes_recv", "protocol"
                ]
            )
        st.session_state.history = pd.concat([st.session_state.history, current_df], ignore_index=True)
        # keep only the last 500 records to limit memory
        if len(st.session_state.history) > 500:
            st.session_state.history = st.session_state.history.iloc[-500:].reset_index(drop=True)

    st.subheader("Recent Network Data (per-interval deltas)")
    if st.session_state.history.empty:
        st.info("Waiting for first interval data. Please keep the page open; the first interval records deltas as 0.")
        return

    st.session_state.history["timestamp"] = pd.to_datetime(st.session_state.history["timestamp"])
    st.dataframe(st.session_state.history.tail(50))

    # Anomaly detection on the per-interval deltas
    # pass only numeric columns required by detector
    try:
        detector_input = st.session_state.history[["bytes_sent", "bytes_recv"]]
    except Exception:
        detector_input = None

    anomaly_df = detect_anomalies(detector_input)

    # if we got anomalies, show them (aligning the result with history)
    if anomaly_df is not None:
        st.subheader("Detected Anomalies and Explanation")
        anomalies = anomaly_df[anomaly_df["anomaly"] == -1]
        st.write(f"Anomalies detected: {len(anomalies)}")
        if not anomalies.empty:
            # join anomaly flags back to recent history rows for display (index alignment)
            recent = st.session_state.history.tail(200).reset_index(drop=True).copy()
            detector_slice = detect_anomalies(recent[["bytes_sent", "bytes_recv"]])
            if detector_slice is not None:
                recent["anomaly"] = detector_slice["anomaly"].values
                st.dataframe(recent[recent["anomaly"] == -1])
            else:
                st.dataframe(anomalies)
            st.warning("Unusual traffic patterns detected. Investigate sources or protocols involved.")
        else:
            st.success("No anomalies in recent data.")

    # protocol distribution across the recorded history
    if "protocol" in st.session_state.history.columns:
        protocol_counts = st.session_state.history["protocol"].value_counts()
        fig_protocol = px.pie(
            values=protocol_counts.values,
            names=protocol_counts.index,
            title="Protocol Distribution in Network Traffic"
        )
        st.plotly_chart(fig_protocol, config=PLOTLY_CONFIG, use_container_width=True)

    # show top IPs by cumulative bytes (use cumulative counters for meaningful totals)
    ip_group = (
        st.session_state.history.groupby("ip_address")[["cum_bytes_sent", "cum_bytes_recv"]]
        .max().sort_values(by="cum_bytes_sent", ascending=False).head(10)
    )
    if not ip_group.empty:
        fig_ips = px.bar(
            ip_group.reset_index(),
            y="cum_bytes_sent",
            x="ip_address",
            title="Top 10 IPs by Cumulative Bytes Sent",
            labels={"ip_address": "IP Address", "cum_bytes_sent": "Cumulative Bytes Sent"}
        )
        st.plotly_chart(fig_ips, config=PLOTLY_CONFIG, use_container_width=True)
