# backend/routes_reports.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from .auth import require_analyst
from .ml import insights
from .auto_report import kpi_summary
from .models import Order
import pandas as pd

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def summary(user=Depends(require_analyst), db: Session = Depends(get_db)):
    # Query all orders from DB
    orders = db.query(Order).all()

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    # Convert to DataFrame
    orders_df = pd.DataFrame([{
        "order_id": o.order_id,
        "customer_id": o.customer_id,
        "order_date": o.order_date,
        "amount": o.amount,
        "product_category": o.product_category,
        "channel": o.channel
    } for o in orders])

    # Pass DataFrame into insights
    data = insights(orders_df)
    kpis = data["kpis"]
    top_cat = max(data["byCategory"], key=lambda x: x["amount"])
    top_chan = max(data["byChannel"], key=lambda x: x["amount"])
    return {"summary": kpi_summary(kpis, top_cat, top_chan)}