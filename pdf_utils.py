from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import pandas as pd
from utils.anomaly import detect_anomalies
import streamlit as st
import plotly.express as px

def generate_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("WiFi Network Anomaly and Statistics Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    df = st.session_state.history.copy()
    if df.empty:
        elements.append(Paragraph("No data available to generate report.", styles["BodyText"]))
        doc.build(elements)
        st.session_state.pdf_report = buffer.getvalue()
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    total_points = len(df)
    max_sent = int(df["bytes_sent"].max())
    max_recv = int(df["bytes_recv"].max())

    elements.append(Paragraph(
        f"Summary:<br/>"
        f"Total data points: <strong>{total_points}</strong><br/>"
        f"Max Bytes Sent (per-interval): <strong>{max_sent}</strong><br/>"
        f"Max Bytes Received (per-interval): <strong>{max_recv}</strong><br/>",
        styles["BodyText"]
    ))

    desc_stats = df[["bytes_sent", "bytes_recv", "cum_bytes_sent", "cum_bytes_recv"]].describe().reset_index()
    stats_data = [[str(x) for x in row] for row in desc_stats.values]
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Statistical Summary", styles["Heading2"]))
    elements.append(Table([desc_stats.columns.tolist()] + stats_data, hAlign='LEFT'))
    elements.append(PageBreak())

    anomaly_df = detect_anomalies(df[["bytes_sent", "bytes_recv"]])
    if anomaly_df is not None:
        df["anomaly"] = anomaly_df["anomaly"]
        elements.append(Paragraph("Detected Anomalies", styles["Heading2"]))
        num_anomalies = int((anomaly_df["anomaly"] == -1).sum())
        num_normals = int((anomaly_df["anomaly"] == 1).sum())
        elements.append(Paragraph(
            f"<strong>{num_anomalies}</strong> anomalies detected; "
            f"<strong>{num_normals}</strong> normal points.<br/>"
            "Below is the list of all detected anomalies with associated statistics.",
            styles["BodyText"]
        ))

        anomaly_rows = anomaly_df[anomaly_df["anomaly"] == -1].copy()
        if not anomaly_rows.empty:
            anomaly_rows = anomaly_rows.reset_index()
            table_cols = ["index", "bytes_sent", "bytes_recv", "anomaly"]
            table_data = [table_cols] + anomaly_rows[table_cols].astype(str).values.tolist()
            elements.append(Spacer(1, 6))
            elements.append(Table(table_data, hAlign='LEFT'))
        else:
            elements.append(Paragraph("No anomalies detected.", styles["BodyText"]))
        elements.append(PageBreak())

    # create charts and embed into PDF
    try:
        fig2d = px.scatter(
            df, x="timestamp", y="bytes_sent", color="interface",
            title="Bytes Sent Over Time", template="plotly_white"
        )
        img1 = fig2d.to_image(format="png")
        img_io1 = BytesIO(img1)
        elements.append(Paragraph("Bytes Sent Over Time", styles["Heading2"]))
        elements.append(Image(img_io1, width=6 * inch, height=4 * inch))
        elements.append(Spacer(1, 12))
    except Exception:
        elements.append(Paragraph("Could not render 2D chart.", styles["BodyText"]))

    try:
        df["timestamp_float"] = df["timestamp"].apply(lambda x: x.timestamp())
        fig3d = px.scatter_3d(
            df, x="bytes_sent", y="bytes_recv", z="timestamp_float", color="interface",
            title="3D Traffic", template="plotly_white"
        )
        img2 = fig3d.to_image(format="png")
        img_io2 = BytesIO(img2)
        elements.append(Paragraph("3D Network Traffic", styles["Heading2"]))
        elements.append(Image(img_io2, width=6 * inch, height=4 * inch))
    except Exception:
        elements.append(Paragraph("Could not render 3D chart.", styles["BodyText"]))

    doc.build(elements)
    st.session_state.pdf_report = buffer.getvalue()
    return st.session_state.pdf_report
