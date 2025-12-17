# auth.py

from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .db import get_db
from .models import User

def get_current_user(x_api_key: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")

    user = db.query(User).filter_by(api_key=x_api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user

def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def require_analyst(user: User = Depends(get_current_user)):
    if user.role not in ["admin", "analyst"]:
        raise HTTPException(status_code=403, detail="Analyst access required")
    return user

def require_viewer(user: User = Depends(get_current_user)):
    # viewers can only read, but no restrictions here
    return user