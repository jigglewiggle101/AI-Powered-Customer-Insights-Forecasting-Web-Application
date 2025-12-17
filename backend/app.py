import io
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import Customer, Order, User
from .ml import compute_rfm, segment_customers, forecast_revenue, insights
from .auth import get_current_user, require_admin, require_analyst, require_viewer
from .routes_analytics import router as analytics_router
from .routes_reports import router as reports_router
from .routes_ml import router as ml_router

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="AI Customer Insights & Forecasting API", version="1.1.0")
app.include_router(ml_router)
app.include_router(analytics_router)
app.include_router(reports_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {"username": user.username, "role": user.role}

@app.post("/upload", dependencies=[Depends(require_admin)])
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    required_cols = {"order_id", "customer_id", "order_date", "amount", "product_category", "channel"}
    if not required_cols.issubset(set(df.columns)):
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {required_cols - set(df.columns)}"
        )

    rows_inserted = 0
    for _, row in df.iterrows():
        existing = db.query(Order).filter_by(order_id=str(row["order_id"])).first()
        if existing:
            continue
        order = Order(
            order_id=str(row["order_id"]),
            customer_id=str(row["customer_id"]),
            order_date=pd.to_datetime(row["order_date"]).to_pydatetime(),
            amount=float(row["amount"]),
            product_category=str(row["product_category"]),
            channel=str(row["channel"]),
        )
        db.add(order)
        rows_inserted += 1

    db.commit()
    return {"rowsInserted": rows_inserted}

@app.get("/insights", dependencies=[Depends(require_analyst)])
def get_insights(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    if not orders:
        return {"message": "No orders found. Upload CSV or seed demo data."}

    df = pd.DataFrame([{
        "order_id": o.order_id,
        "customer_id": o.customer_id,
        "order_date": o.order_date,
        "amount": o.amount,
        "product_category": o.product_category,
        "channel": o.channel
    } for o in orders])

    return insights(df)

@app.get("/segments", dependencies=[Depends(require_analyst)])
def get_segments(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    if not orders:
        return {"segments": []}

    df = pd.DataFrame([{
        "order_id": o.order_id,
        "customer_id": o.customer_id,
        "order_date": o.order_date,
        "amount": o.amount,
    } for o in orders])

    rfm = compute_rfm(df)
    seg = segment_customers(rfm)
    return {"segments": seg.to_dict(orient="records")}

@app.get("/forecast", dependencies=[Depends(require_viewer)])
def get_forecast(days: int = 30, db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    if not orders:
        return {"forecast": []}

    df = pd.DataFrame([{
        "order_date": o.order_date,
        "amount": o.amount,
    } for o in orders])

    fc = forecast_revenue(df, periods=days)
    return {"forecast": fc.to_dict(orient="records")}

@app.post("/seed", dependencies=[Depends(require_admin)])
def seed_demo():
    from .seed import seed
    seed()
    return {"status": "seeded"}

