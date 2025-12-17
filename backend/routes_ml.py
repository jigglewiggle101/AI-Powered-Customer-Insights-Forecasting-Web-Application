# backend/routes_ml.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from .auth import require_analyst
from .ml_churn import train_churn, predict_churn

router = APIRouter(prefix="/ml", tags=["ml"])

@router.post("/churn/train")
def churn_train(user=Depends(require_analyst), db: Session = Depends(get_db)):
    return train_churn(db)

@router.get("/churn/predict")
def churn_predict(user=Depends(require_analyst), db: Session = Depends(get_db)):
    try:
        return {"results": predict_churn(db)}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))