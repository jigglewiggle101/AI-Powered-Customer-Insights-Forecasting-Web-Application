# backend/analytics_anomalies.py
import pandas as pd
from sqlalchemy.orm import Session
from .models import Order

def daily_revenue_df(db: Session) -> pd.DataFrame:
    rows = db.query(Order).all()
    df = pd.DataFrame([{"date": o.order_date.date(), "amount": float(o.amount)} for o in rows])
    if df.empty:
        return pd.DataFrame(columns=["date", "amount"])
    return df.groupby("date", as_index=False)["amount"].sum()

def detect_anomalies(db: Session, z_thresh: float = 2.0):
    df = daily_revenue_df(db)
    if df.empty:
        return []
    mean = df["amount"].mean()
    std = df["amount"].std() or 1.0
    df["z"] = (df["amount"] - mean) / std
    df["is_anomaly"] = df["z"].abs() >= z_thresh
    anomalies = df[df["is_anomaly"]].sort_values("date", ascending=False)
    return anomalies.to_dict(orient="records")