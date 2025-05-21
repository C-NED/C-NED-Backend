from sqlalchemy.orm import Session
from app.models.db_model.path import Path
from shapely.geometry import Point as ShapelyPoint

def save_paths(db: Session, path: list, navigation_id: int):
    path_list = []
    for idx, coords in enumerate(path):
        path_obj = Path(
            navigation_id=navigation_id,
            pathidx=idx,
            path_loc=ShapelyPoint(coords[0], coords[1]),
            step_order=idx + 1
        )
        db.add(path_obj)
        path_list.append(path_obj)

    db.flush()  # ✅ 추가해줘야 path_id가 자동 채워짐
    return path_list

