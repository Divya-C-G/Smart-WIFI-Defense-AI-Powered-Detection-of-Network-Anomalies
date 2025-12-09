import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    """
    Expects df with numeric 'bytes_sent' and 'bytes_recv' columns (per-interval delta).
    Returns a copy of df with 'anomaly' column (1 normal, -1 anomaly) or None if insufficient data.
    """
    if df is None or len(df) < 10:
        return None
    df = df.copy()
    # ensure integer/float types
    df["bytes_sent"] = pd.to_numeric(df["bytes_sent"], errors="coerce").fillna(0)
    df["bytes_recv"] = pd.to_numeric(df["bytes_recv"], errors="coerce").fillna(0)

    # IsolationForest is sensitive to scale; combine features as-is (small app)
    clf = IsolationForest(contamination=0.05, random_state=42)
    try:
        preds = clf.fit_predict(df[["bytes_sent", "bytes_recv"]])
    except Exception:
        # if something fails (e.g., constant columns), return None
        return None
    df["anomaly"] = preds
    return df
