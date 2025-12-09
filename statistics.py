import streamlit as st
import pandas as pd
import plotly.express as px
from utils.anomaly import detect_anomalies

def statistics():
    st.title("📈 Statistical Analysis")

    df = st.session_state.history.copy()
    if df is None or df.empty:
        st.info("No data to analyze yet.")
        return

    # Fix: import pandas allows using pd.to_datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.dataframe(df.describe(include="all"))

    anomaly_df = detect_anomalies(df[["bytes_sent", "bytes_recv"]])
    if anomaly_df is not None:
        st.subheader("Anomalies")
        st.dataframe(anomaly_df[["bytes_sent","bytes_recv","anomaly"]])

        counts = anomaly_df["anomaly"].value_counts()
        fig = px.pie(
            names=["Normal","Anomaly"],
            values=[counts.get(1,0), counts.get(-1,0)],
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
