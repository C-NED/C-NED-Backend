# routes/navigation.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.db_model.navigation import Navigation
from app.models.db_model.guide import Guide
from app.models.db_model.path import Path
from sqlalchemy.orm import Session
from app.database import get_db  # get_db 경로는 실제 경로에 맞게
from app.key_collection import REDIS_URL
import redis

router = APIRouter()

r = redis.from_url(
    REDIS_URL,
    decode_responses=True  # string 자동 디코딩
)

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

@router.post("/user/navigation/{nav_id}/preload_path")
def preload_path(nav_id: int, db: Session = Depends(get_db)):
    path_rows = db.query(Path).filter(Path.navigation_id == nav_id).all()
    guide = db.query(Guide).filter(Guide.navigation_id == nav_id).all()

    if not path_rows or not guide:
        raise HTTPException(status_code=404, detail="경로 또는 안내 없음")

    guide_indices = [g.pointidx for g in guide]
    extended = set(i + d for i in guide_indices for d in [-1, 0, 1])

    guide_path = [
        {"pathidx": p.pathidx, "point": p.path_loc}
        for p in path_rows if p.pathidx in extended
    ]

    r.set(f"navigation:{nav_id}:guide_path", json.dumps(guide_path), ex=3600)
    return {"message": f"navigation {nav_id} path 캐싱 완료", "count": len(guide_path)}


@router.get("/user/navigation/{nav_id}/get_cached_path")
def get_cached_path(nav_id: int):
    key = f"navigation:{nav_id}:guide_path"
    cached = r.get(key)

    if not cached:
        raise HTTPException(status_code=404, detail="캐시된 경로 없음")

    return json.loads(cached)
