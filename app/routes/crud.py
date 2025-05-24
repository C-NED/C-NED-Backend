# routes/navigation.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.db_model.navigation import Navigation
from app.models.db_model.guide import Guide
from app.models.db_model.user import User
from app.models.db_model.favorite_place import FavoritePlace
from app.models.db_model.path import Path
from app.models.db_model.caution import Caution
from app.models.db_model.dangerous_incident import DangerousIncident
from app.models.db_model.outbreak import Outbreak
from app.models.db_model.vsl import Vsl
from app.models.common.schemas import CrudRequest
from sqlalchemy.orm import Session
from app.database import get_db  # get_db 경로는 실제 경로에 맞게
from app.key_collection import REDIS_URL
import redis
import json

router = APIRouter()

r = redis.from_url(
    REDIS_URL,
    decode_responses=True  # string 자동 디코딩
)

try:
    pong = r.ping()
    print("Redis 연결 성공!" if pong else "Redis 연결 실패!")
except Exception as e:
    print("Redis 연결 오류:", e)

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
    guide = db.query(Guide).filter(Guide.navigation_id == nav_id).all()
    if not guide:
        raise HTTPException(status_code=404, detail="안내 정보 없음")

    guide_indices = [g.pointidx for g in guide]
    extended = set(i + d for i in guide_indices for d in [-1, 0, 1])

    # pathidx, path_loc, step_order만 가져옴 (tuple 형태로 반환됨)
    path_rows = db.query(Path.pathidx, Path.path_loc,Path.step_order)\
                  .filter(Path.navigation_id == nav_id)\
                  .filter(Path.pathidx.in_(extended))\
                  .all()

    if not path_rows:
        raise HTTPException(status_code=404, detail="경로 없음")

    # Redis에 저장할 포맷으로 변환
    guide_path = [
        {"pathidx": pathidx, "point": path_loc, "step_order": step_order}
        for pathidx, path_loc, step_order in path_rows
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


# crud_map.py

# from models import Risk

TableMap = {
    "user": User,
    "guide": Guide,
    "navigation": Navigation,
    "caution": Caution,
    "Dincident": DangerousIncident,
    "outbreak": Outbreak,
    "vsl": Vsl,
    "favorite_place": FavoritePlace,
    "path": Path
}

#일단 risk 테이블 제외

@router.post("/admin")
async def dynamic_crud(req: CrudRequest, db: Session = Depends(get_db)):
    Model = TableMap.get(req.table)
    if not Model:
        raise HTTPException(status_code=400, detail="Invalid table name")

    if req.action == "read":
        query = db.query(Model)
        if req.filter:
            for key, value in req.filter.items():
                query = query.filter(getattr(Model, key) == value)
        results = query.all()
        return {"success": True, "data": [row.__dict__ for row in results]}

    elif req.action == "create":
        instance = Model(**req.data)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return {"success": True, "data": instance.__dict__}

    elif req.action == "update":
        query = db.query(Model)
        if not req.filter:
            raise HTTPException(status_code=400, detail="Missing filter for update")
        for key, value in req.filter.items():
            query = query.filter(getattr(Model, key) == value)
        instance = query.first()
        if not instance:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in req.data.items():
            setattr(instance, key, value)
        db.commit()
        db.refresh(instance)
        return {"success": True, "data": instance.__dict__}

    elif req.action == "delete":
        query = db.query(Model)
        if not req.filter:
            raise HTTPException(status_code=400, detail="Missing filter for delete")
        for key, value in req.filter.items():
            query = query.filter(getattr(Model, key) == value)
        instance = query.first()
        if not instance:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(instance)
        db.commit()
        return {"success": True}

    else:
        raise HTTPException(status_code=400, detail="Invalid action")
