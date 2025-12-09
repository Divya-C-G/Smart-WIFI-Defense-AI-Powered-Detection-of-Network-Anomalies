import streamlit as st
import plotly.express as px
import pandas as pd
from utils.constants import PLOTLY_CONFIG

def visualization():
    st.title("📊 Network Data Visualization")
    df = st.session_state.history.copy()
    if df.empty:
        st.info("No network data to visualize. Please use the real-time monitor first.")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # plot per-interval bytes_sent over time
    fig2d = px.scatter(
        df,
        x="timestamp",
        y="bytes_sent",
        color="interface",
        symbol="interface",
        title="Bytes Sent (per-interval) Over Time",
        labels={"bytes_sent": "Bytes Sent (per-interval)", "timestamp": "Time", "interface": "Interface"},
        template="plotly_dark",
    )
    fig2d.update_traces(marker=dict(size=10, line=dict(width=1)))
    fig2d.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        legend=dict(title="Interface", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig2d, config=PLOTLY_CONFIG, use_container_width=True)

    df["timestamp_float"] = df["timestamp"].apply(lambda x: x.timestamp())
    fig3d = px.scatter_3d(
        df,
        x="bytes_sent",
        y="bytes_recv",
        z="timestamp_float",
        color="interface",
        title="3D Network Traffic (per-interval)",
        labels={
            "bytes_sent": "Bytes Sent",
            "bytes_recv": "Bytes Received",
            "timestamp_float": "Time"
        },
        template="plotly_dark",
    )
    fig3d.update_traces(marker=dict(size=6))
    fig3d.update_layout(
        scene=dict(
            xaxis_title="Bytes Sent",
            yaxis_title="Bytes Received",
            zaxis_title="Time",
        ),
        legend=dict(title="Interface")
    )
    st.plotly_chart(fig3d, config=PLOTLY_CONFIG, use_container_width=True)
