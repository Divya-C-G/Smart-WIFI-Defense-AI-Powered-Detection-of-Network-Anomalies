import streamlit as st
from utils.ui_utils import load_css, show_quote
from utils.constants import PLOTLY_CONFIG

# Initialize page
st.set_page_config(page_title="WiFi Guardian 🛡", page_icon="📶", layout="wide")
load_css()

# Initialize session state defaults
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "history" not in st.session_state:
    import pandas as pd
    st.session_state.history = pd.DataFrame(
        columns=[
            "timestamp", "interface", "ip_address", "location",
            "bytes_sent", "bytes_recv", "cum_bytes_sent", "cum_bytes_recv", "protocol"
        ]
    )
if "pdf_report" not in st.session_state:
    st.session_state.pdf_report = None
if "prev_counters" not in st.session_state:
    st.session_state.prev_counters = {}

# Sidebar navigation (keeps the exact button-driven behaviour)
with st.sidebar:
    st.title("🔍 Navigation")
    st.markdown("---")
    if st.button("📤 1. Real-time Monitor"):
        st.session_state.current_step = 1
    if st.button("📊 2. Data Visualization", disabled=st.session_state.history.empty):
        st.session_state.current_step = 2
    if st.button("📈 3. Statistics Analysis", disabled=st.session_state.history.empty):
        st.session_state.current_step = 3
    if st.button("📥 4. Download Report", disabled=st.session_state.history.empty):
        st.session_state.current_step = 4

# Page dispatching (import delayed to avoid heavy imports when not needed)
if st.session_state.current_step == 1:
    from modules.realtime import real_time_monitor
    real_time_monitor()
elif st.session_state.current_step == 2:
    from modules.visualization import visualization
    visualization()
elif st.session_state.current_step == 3:
    from modules.statistics import statistics
    statistics()
elif st.session_state.current_step == 4:
    from modules.download import download
    download()
