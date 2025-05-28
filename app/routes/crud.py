# routes/navigation.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.db_model.navigation import Navigation
from app.models.db_model.guide import Guide
from app.models.db_model.user import User
from app.models.db_model.admin import Admin
from app.models.db_model.favorite_place import FavoritePlace
from app.models.db_model.path import Path
from app.models.db_model.road_info import RoadInfo
from app.models.db_model.road_section import RoadSection
from app.models.db_model.caution import Caution
from app.models.db_model.dangerous_incident import DangerousIncident
from app.models.db_model.outbreak import Outbreak
from app.models.db_model.vsl import Vsl
from app.models.common.schemas import CrudRequest
from sqlalchemy.orm import Session
from app.database import get_db  # get_db 경로는 실제 경로에 맞게
import json
from app.redis_setup import r  # Redis 클라이언트 인스턴스


router = APIRouter()

# r = redis.from_url(
#     REDIS_URL,
#     decode_responses=True  # string 자동 디코딩
# )


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

    # 🔥 출발점 & 도착점 포함시키기
    start_path = db.query(Path.pathidx).filter(Path.navigation_id == nav_id).order_by(Path.step_order.asc()).first()
    end_path = db.query(Path.pathidx).filter(Path.navigation_id == nav_id).order_by(Path.step_order.desc()).first()

    if start_path:
        extended.add(start_path[0])
    if end_path:
        extended.add(end_path[0])

    # pathidx, path_loc, step_order 가져오기
    path_rows = db.query(Path.pathidx, Path.path_loc, Path.step_order)\
                  .filter(Path.navigation_id == nav_id)\
                  .filter(Path.pathidx.in_(extended))\
                  .all()

    if not path_rows:
        raise HTTPException(status_code=404, detail="경로 없음")

    guide_path = [
        {"pathidx": pathidx, "point": path_loc, "step_order": step_order}
        for pathidx, path_loc, step_order in path_rows
    ]

    # Redis에 저장
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
    "admin": Admin,
    "road_section":RoadSection,
    "caution": Caution,
    "dincident": DangerousIncident,
    "outbreak": Outbreak,
    "vsl": Vsl,
    "favorite_place": FavoritePlace,
    "path": Path,
    "road_info":RoadInfo,
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


# alert 캐싱 API
@router.post("/user/navigation/{nav_id}/preload_alerts")
def preload_alerts(nav_id: int, db: Session = Depends(get_db)):
    alert_config = {
        "outbreak": {
            "model": Outbreak,
            "fields": ["event_type", "period", "message", "loc"]
        },
        "vsl": {
            "model": Vsl,
            "fields": ["loc", "default_speed_limit", "cur_speed_limit"]
        },
        "dincident": {
            "model": DangerousIncident,
            "fields": ["loc", "period"]
        },
        "caution": {
            "model": Caution,
            "fields": ["message", "loc"]
        },
    }

    alert_data = {}

    for key, config in alert_config.items():
        Model = config["model"]
        fields = config["fields"]

        rows = db.query(Model).filter(Model.navigation_id == nav_id).all()
        if not rows:
            continue

        filtered_rows = []
        for row in rows:
            data = {}
            for field in fields:
                value = getattr(row, field, None)
                if hasattr(value, "isoformat"):
                    value = value.isoformat()
                data[field] = value
            filtered_rows.append(data)

        alert_data[key] = filtered_rows

    if not alert_data:
        raise HTTPException(status_code=404, detail="해당 경로에 알림 정보 없음")

    r.set(f"navigation:{nav_id}:alert", json.dumps(alert_data), ex=3600)
    return {
        "message": f"navigation {nav_id} alert 정보 캐싱 완료",
        "keys": list(alert_data.keys()),
        "count": {k: len(v) for k, v in alert_data.items()}
    }

#alert 조회 API
@router.get("/user/navigation/{nav_id}/get_cached_alerts")
def get_cached_alerts(nav_id: int):
    key = f"navigation:{nav_id}:alert"  # ← 저장 시 일치시키기
    cached = r.get(key)

    if not cached:
        raise HTTPException(status_code=404, detail="캐시된 경고 없음")

    try:
        data = json.loads(cached)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"캐시 파싱 오류: {e}")

    # 반환 형식 표준화: 모든 키 포함, 누락 시 빈 배열
    expected_keys = ["outbreak", "vsl", "dincident", "caution"]
    result = {key: data.get(key, []) for key in expected_keys}

    return result


def estimate_lane_count(road_name: str) -> int:
    if "고속도로" in road_name or "순환로" in road_name:
        return 4
    if "대로" in road_name:
        return 4
    if "로" in road_name:
        return 2
    return 2  # 기본값
    # 기본적으로 2차선으로 추정, 필요시 로직 확장 가능

# 차선 정보 캐싱 API
@router.post("/user/navigation/{nav_id}/preload_road_info", response_model=None)
def preload_path_with_lane(nav_id: int, db: Session = Depends(get_db)):

    road_sections = (
        db.query(RoadSection.pointidx, RoadSection.name)
        .filter(RoadSection.navigation_id == nav_id)
        .all()
    )

    response_list = []
    for section in road_sections:
        lane_count = estimate_lane_count(section.name or "")
        response_list.append({
            "pointidx": section.pointidx,
            "road_name": section.name,
            "lane_count": lane_count
        })

    r.set(f"navigation:{nav_id}:lane", json.dumps(response_list), ex=7200)

    return {"status": "ok", "count": len(response_list)}

# 차선 정보 조회 API
@router.get("/user/navigation/{nav_id}/get_cached_road_info")
def get_cached_road_info(nav_id: int):
    key = f"navigation:{nav_id}:lane_estimation"
    cached = r.get(key)

    if not cached:
        raise HTTPException(status_code=404, detail="캐시된 도로 정보 없음")

    try:
        data = json.loads(cached)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"캐시 파싱 오류: {e}")

    return data

# 전체 경로 정보 캐싱 API
@router.post("/user/navigation/{nav_id}/preload_all")
def preload_all(nav_id: int, db: Session = Depends(get_db)):
    preload_path(nav_id, db)
    preload_alerts(nav_id, db)
    preload_road_info(nav_id, db)
    return {"status": "ok"}

# 전체 경로 정보 조회 API
@router.get("/user/navigation/{nav_id}/get_cached_all")
def get_cached_all(nav_id: int):
    path_key = f"navigation:{nav_id}:guide_path"
    alert_key = f"navigation:{nav_id}:alert"
    road_info_key = f"navigation:{nav_id}:lane_estimation"

    cached_path = r.get(path_key)
    cached_alerts = r.get(alert_key)
    cached_road_info = r.get(road_info_key)

    if not cached_path or not cached_alerts or not cached_road_info:
        raise HTTPException(status_code=404, detail="캐시된 정보 없음")

    try:
        path_data = json.loads(cached_path)
        alert_data = json.loads(cached_alerts)
        road_info_data = json.loads(cached_road_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"캐시 파싱 오류: {e}")

    return {
        "path": path_data,
        "alerts": alert_data,
        "lane": road_info_data
    }