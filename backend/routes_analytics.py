# backend/routes_analytics.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .db import get_db
from .auth import require_analyst
from .analytics_anomalies import detect_anomalies

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/anomalies")
def anomalies(user=Depends(require_analyst), db: Session = Depends(get_db), z: float = 2.0):
    return {"anomalies": detect_anomalies(db, z_thresh=z)}