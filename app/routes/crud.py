# routes/navigation.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.db_model.navigation import Navigation
from app.models.db_model.guide import Guide
from sqlalchemy.orm import Session
from app.database import get_db  # get_db 경로는 실제 경로에 맞게

router = APIRouter()

@router.get("/user/navigation/guide/{navigation_id}")
def get_guide_by_navigation_id(navigation_id: int,db: Session = Depends(get_db) ):
    guide_steps = db.query(Guide).filter(Guide.navigation_id == navigation_id).order_by(Guide.step_order).all()
    if not guide_steps:
        raise HTTPException(status_code=404, detail="guide not found")

    return {
        "navigation_id": navigation_id,
        "guide": [
            {
                "pointidx": step.pointidx,
                "instructions": step.instructions,
                "distance": step.distance,
                "duration": step.duration,
                "step_order": step.step_order,  # [lon, lat]
            }
            for step in guide_steps
        ]
    }
