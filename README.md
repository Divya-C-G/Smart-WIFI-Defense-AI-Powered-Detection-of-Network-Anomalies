# Wi-Fi Guardian 🛡

Wi-Fi Guardian is a real-time Wi-Fi network monitoring and anomaly detection tool built with Streamlit. It allows you to monitor network traffic, visualize statistics, detect anomalies, and generate PDF reports for analysis.

---

## 🚀 Features

- **Real-Time Monitoring:** Monitor per-interface network traffic (bytes sent/received) in real time.  
- **Protocol Analysis:** Identify protocol distribution (TCP, UDP, ICMP, etc.).  
- **Anomaly Detection:** Detect unusual traffic patterns using Isolation Forest.  
- **Data Visualization:** 2D and 3D plots for network traffic over time.  
- **PDF Report Generation:** Export statistics and anomalies as a PDF report.  
- **Simple Navigation:** Use sidebar buttons to switch between Monitor, Visualization, Statistics, and Download.  

---

## 📁 Project Structure

MajorProject/
│
├── app.py # Main Streamlit app controlling navigation
├── requirements.txt # Python dependencies
├── .gitignore # Recommended git ignore file
│
├── modules/ # Core app functionality
│ ├── init.py
│ ├── realtime.py # Real-time monitoring logic
│ ├── visualization.py # 2D & 3D plots
│ ├── statistics.py # Anomaly detection & statistical analysis
│ ├── download.py # PDF report download
│
└── utils/ # Utility functions
├── init.py
├── network_utils.py # Network helpers
├── anomaly.py # Anomaly detection helpers
├── pdf_utils.py # PDF generation helpers
├── ui_utils.py # UI helpers and quotes



---

## 💻 Installation

### 1. Clone the repository


git clone https://github.com/<your-username>/MajorProject.git
cd MajorProject

### 2. Create a virtual environment
python -m venv venv

###3. Activate the virtual environment
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

### 4. Install dependencies
pip install -r requirements.txt

🏃 Run the App
streamlit run app.py

Open the Local URL (e.g., http://localhost:8501) in your browser.

Use the sidebar to navigate:

📤 Real-Time Monitor

📊 Data Visualization

📈 Statistics Analysis

📥 Download Report

⚡ Notes

Requires a working internet connection for IP geolocation.

Works best with Wi-Fi interfaces; other network interfaces may show limited stats.

For large datasets, 3D plotting may be slower.

📝 Requirements

Python 3.11+

See requirements.txt for full dependencies
