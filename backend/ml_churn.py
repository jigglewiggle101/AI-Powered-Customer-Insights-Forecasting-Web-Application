# # backend/ml_churn.py
# import pandas as pd
# from sqlalchemy.orm import Session
# from .models import Order, Customer
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression

# model = None
# scaler = None
# feature_cols = ["recency", "frequency", "monetary"]

# def build_features(db: Session) -> pd.DataFrame:
#     # RFM from your DB
#     customers = db.query(Customer).all()
#     rows = []
#     for c in customers:
#         rows.append({
#             "customer_id": c.customer_id,
#             "recency": c.recency_days,
#             "frequency": c.order_count,
#             "monetary": float(c.total_spend or 0.0),
#             # Simple label: churn if no order in last 60 days
#             "churn": 1 if (c.recency_days or 9999) > 60 else 0
#         })
#     return pd.DataFrame(rows)

# def train_churn(db: Session):
#     global model, scaler
#     df = build_features(db)
#     X = df[feature_cols].fillna(0.0).values
#     y = df["churn"].values
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)

#     scaler = StandardScaler()
#     X_train_scaled = scaler.fit_transform(X_train)
#     model = LogisticRegression(max_iter=1000)
#     model.fit(X_train_scaled, y_train)
#     acc = model.score(scaler.transform(X_test), y_test)
#     return {"status": "trained", "accuracy": round(acc, 4)}

# def predict_churn(db: Session):
#     global model, scaler
#     if model is None or scaler is None:
#         raise RuntimeError("Model not trained")
#     df = build_features(db)
#     X_scaled = scaler.transform(df[feature_cols].fillna(0.0).values)
#     probs = model.predict_proba(X_scaled)[:, 1]
#     df["churn_probability"] = probs
#     # Top‑N risky customers
#     out = df.sort_values("churn_probability", ascending=False).head(50)[
#         ["customer_id", "recency", "frequency", "monetary", "churn_probability"]
#     ]
#     return out.to_dict(orient="records")

# backend/ml_churn.py

import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from .models import Order, Customer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

model = None
scaler = None
feature_cols = ["recency", "frequency", "monetary"]

def build_features(db: Session) -> pd.DataFrame:
    """Build RFM features for churn prediction from orders."""
    now = datetime.utcnow()
    rows = []
    customers = db.query(Customer).all()

    for c in customers:
        # get all orders for this customer
        orders = db.query(Order).filter(Order.customer_id == c.customer_id).all()
        if orders:
            last_order_date = max(o.order_date for o in orders)
            recency_days = (now - last_order_date).days
            frequency = len(orders)
            monetary = sum(float(o.amount or 0.0) for o in orders)
        else:
            recency_days = 9999
            frequency = 0
            monetary = 0.0

        rows.append({
            "customer_id": c.customer_id,
            "recency": recency_days,
            "frequency": frequency,
            "monetary": monetary,
            "churn": 1 if recency_days > 60 else 0
        })

    return pd.DataFrame(rows)

def train_churn(db: Session):
    global model, scaler
    df = build_features(db)
    if df.empty:
        return {"status": "failed", "reason": "No customers found"}

    X = df[feature_cols].fillna(0.0).values
    y = df["churn"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)
    acc = model.score(scaler.transform(X_test), y_test)

    return {"status": "trained", "accuracy": round(acc, 4)}

def predict_churn(db: Session):
    global model, scaler
    if model is None or scaler is None:
        raise RuntimeError("Model not trained")

    df = build_features(db)
    if df.empty:
        return []

    X_scaled = scaler.transform(df[feature_cols].fillna(0.0).values)
    probs = model.predict_proba(X_scaled)[:, 1]
    df["churn_probability"] = probs

    # Top‑N risky customers
    out = df.sort_values("churn_probability", ascending=False).head(50)[
        ["customer_id", "recency", "frequency", "monetary", "churn_probability"]
    ]
    return out.to_dict(orient="records")