import streamlit as st
import random

PIO_SETTINGS = {
    # kept empty here; plotting style controlled in each module
}

QUOTES = [
    "🛡 Cybersecurity is not a product, but a process!",
    "🔒 Better safe than hacked!",
    "📶 A secure network is a happy network!",
    "🤖 AI guards while you sleep!",
    "🚨 Detect before you regret!",
    "💻 Security is always worth the investment!",
    "🔍 Stay vigilant, stay secure!"
]

def load_css():
    st.markdown("""
    <style>
        .st-emotion-cache-1kyxreq { display: flex; flex-flow: wrap; gap: 2rem; }
        .reportview-container .main .block-container { padding-top: 2rem; }
        .sidebar .sidebar-content { background: linear-gradient(180deg, #2e3b4e, #1a2639); }
        .stButton>button { width: 100%; margin: 5px 0; transition: all 0.3s; }
        .stButton>button:hover { transform: scale(1.05); }
        .summary-box { padding: 20px; border-radius: 10px; background-color: #2e3b4e; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

def show_quote():
    st.markdown(f"<h3 style='text-align: center; color: #4CAF50;'>{random.choice(QUOTES)}</h3>", unsafe_allow_html=True)
