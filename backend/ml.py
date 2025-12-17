# #ml:

# import pandas as pd
# import numpy as np
# from datetime import timedelta
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans

# try:
#     from prophet import Prophet
#     HAS_PROPHET = False  
# except Exception:
#     HAS_PROPHET = False

# def compute_rfm(orders_df: pd.DataFrame, now: pd.Timestamp | None = None):
#     if now is None:
#         now = pd.Timestamp.utcnow().tz_localize(None)  # force tz-naive
#     orders_df["order_date"] = pd.to_datetime(orders_df["order_date"]).dt.tz_localize(None)
#     rfm = orders_df.groupby("customer_id").agg({
#         "order_date": lambda x: (now - x.max()).days,
#         "order_id": "count",
#         "amount": "sum"
#     }).rename(columns={"order_date": "recency", "order_id": "frequency", "amount": "monetary"}).reset_index()
#     return rfm

# def segment_customers(rfm: pd.DataFrame, n_clusters: int = 4):
#     scaler = StandardScaler()
#     X = scaler.fit_transform(rfm[["recency", "frequency", "monetary"]])
#     kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
#     rfm["segment_label"] = kmeans.fit_predict(X)
#     # Simple human-readable mapping
#     labels = {0: "High value", 1: "Loyal", 2: "At risk", 3: "New/Low value"}
#     rfm["segment"] = rfm["segment_label"].map(lambda x: labels.get(x, f"Segment {x}"))
#     return rfm

# def forecast_revenue(orders_df: pd.DataFrame, periods: int = 30):
#     # Build daily revenue series
#     orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
#     daily = orders_df.groupby(pd.Grouper(key="order_date", freq="D")).agg({"amount": "sum"}).reset_index()
#     daily.rename(columns={"order_date": "ds", "amount": "y"}, inplace=True)

#     if len(daily) < 7:
#         # Not enough data; naive projection
#         last_val = daily["y"].iloc[-1] if len(daily) else 0.0
#         future_dates = pd.date_range(daily["ds"].max() + timedelta(days=1) if len(daily) else pd.Timestamp.utcnow(), periods=periods)
#         return pd.DataFrame({"ds": future_dates, "yhat": [last_val] * periods})

#     if HAS_PROPHET:
#         m = Prophet()
#         m.fit(daily)
#         future = m.make_future_dataframe(periods=periods)
#         forecast = m.predict(future)
#         return forecast[["ds", "yhat"]].tail(periods)
#     else:
#         # Fallback: moving average forecast
#         daily["yhat"] = daily["y"].rolling(window=min(7, len(daily))).mean().bfill()
#         last_date = daily["ds"].max()
#         future_dates = [last_date + timedelta(days=i) for i in range(1, periods + 1)]
#         last_ma = daily["yhat"].iloc[-1]
#         return pd.DataFrame({"ds": future_dates, "yhat": [float(last_ma)] * periods})
    
    
    

# def insights(orders_df: pd.DataFrame):
#     # Simple KPIs
#     total_revenue = float(orders_df["amount"].sum())
#     avg_order_value = float(orders_df["amount"].mean()) if len(orders_df) else 0.0
#     customers = orders_df["customer_id"].nunique()
#     orders = len(orders_df)
#     # Category split
#     category_rev = orders_df.groupby("product_category")["amount"].sum().sort_values(ascending=False).reset_index()
#     # Channel split
#     channel_rev = orders_df.groupby("channel")["amount"].sum().sort_values(ascending=False).reset_index()
#     return {
#         "kpis": {
#             "totalRevenue": total_revenue,
#             "avgOrderValue": avg_order_value,
#             "customers": int(customers),
#             "orders": int(orders)
#         },
#         "byCategory": category_rev.to_dict(orient="records"),
#         "byChannel": channel_rev.to_dict(orient="records")
#     }

# backend/ml.py

import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Correct Prophet detection
try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False


def compute_rfm(orders_df: pd.DataFrame, now: pd.Timestamp | None = None):
    if now is None:
        now = pd.Timestamp.utcnow().tz_localize(None)  # force tz-naive
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"]).dt.tz_localize(None)
    rfm = orders_df.groupby("customer_id").agg({
        "order_date": lambda x: (now - x.max()).days,
        "order_id": "count",
        "amount": "sum"
    }).rename(columns={
        "order_date": "recency",
        "order_id": "frequency",
        "amount": "monetary"
    }).reset_index()
    return rfm


def segment_customers(rfm: pd.DataFrame, n_clusters: int = 4):
    scaler = StandardScaler()
    X = scaler.fit_transform(rfm[["recency", "frequency", "monetary"]])
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    rfm["segment_label"] = kmeans.fit_predict(X)
    # Simple human-readable mapping
    labels = {0: "High value", 1: "Loyal", 2: "At risk", 3: "New/Low value"}
    rfm["segment"] = rfm["segment_label"].map(lambda x: labels.get(x, f"Segment {x}"))
    return rfm


def forecast_revenue(orders_df: pd.DataFrame, periods: int = 30):
    # Build daily revenue series
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
    daily = orders_df.groupby(pd.Grouper(key="order_date", freq="D")).agg({"amount": "sum"}).reset_index()
    daily.rename(columns={"order_date": "ds", "amount": "y"}, inplace=True)

    # Debug: show last 10 days of input
    print("Last 10 days of daily revenue:")
    print(daily.tail(10))

    if len(daily) < 7:
        # Not enough data; naive projection
        last_val = daily["y"].iloc[-1] if len(daily) else 0.0
        future_dates = pd.date_range(
            daily["ds"].max() + timedelta(days=1) if len(daily) else pd.Timestamp.utcnow(),
            periods=periods
        )
        return pd.DataFrame({"ds": future_dates, "yhat": [last_val] * periods})

    if HAS_PROPHET:
        m = Prophet()
        m.fit(daily)
        future = m.make_future_dataframe(periods=periods)
        forecast = m.predict(future)
        return forecast[["ds", "yhat"]].tail(periods)
    else:
        # Fallback: moving average forecast
        daily["yhat"] = daily["y"].rolling(window=min(7, len(daily))).mean().bfill()
        last_date = daily["ds"].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, periods + 1)]
        last_ma = daily["yhat"].iloc[-1]
        return pd.DataFrame({"ds": future_dates, "yhat": [float(last_ma)] * periods})


def insights(orders_df: pd.DataFrame):
    # Simple KPIs
    total_revenue = float(orders_df["amount"].sum())
    avg_order_value = float(orders_df["amount"].mean()) if len(orders_df) else 0.0
    customers = orders_df["customer_id"].nunique()
    orders = len(orders_df)
    # Category split
    category_rev = orders_df.groupby("product_category")["amount"].sum().sort_values(ascending=False).reset_index()
    # Channel split
    channel_rev = orders_df.groupby("channel")["amount"].sum().sort_values(ascending=False).reset_index()
    return {
        "kpis": {
            "totalRevenue": total_revenue,
            "avgOrderValue": avg_order_value,
            "customers": int(customers),
            "orders": int(orders)
        },
        "byCategory": category_rev.to_dict(orient="records"),
        "byChannel": channel_rev.to_dict(orient="records")
    }