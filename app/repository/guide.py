from sqlalchemy.orm import Session
from app.models.db_model.guide import Guide
from app.models.db_model.path import Path

def save_guide(db: Session, guides: dict,navigation_id:int) :
   for i, g in enumerate(guides):
    point_index = g["pointIndex"]
    if point_index is None:
       print("pointidx is not exist")

    path = db.query(Path).filter_by(
            navigation_id=navigation_id,  # 명시적으로 필터!
            pathidx=point_index
        ).first()

    if not path:
        print(f"⚠️  Path not found for pointIndex={point_index}")
        continue

    guide = Guide(
        navigation_id=navigation_id,  # ✅ 여기서 바로 가져오기
        pointidx=point_index,
        step_order=i + 1,
        instructions=g["instructions"],
        distance=g["distance"],
        duration=g["duration"]
    )
    db.add(guide)
