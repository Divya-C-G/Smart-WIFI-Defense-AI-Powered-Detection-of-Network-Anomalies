import streamlit as st
from utils.pdf_utils import generate_pdf
import base64

def download():
    st.title("📥 Download PDF Report")
    if st.button("Generate Report"):
        generate_pdf()
        st.success("Report generated!")
        if st.session_state.pdf_report:
            b64 = base64.b64encode(st.session_state.pdf_report).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="wifi_report.pdf">Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
