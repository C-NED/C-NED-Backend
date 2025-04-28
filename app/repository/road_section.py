from sqlalchemy.orm import Session
from app.models.db_model.road_section import RoadSection

CONGESTION_MAP = {
    0: "정보 없음",
    1: "원활",
    2: "서행",
    3: "혼잡"
}

def save_road_sections(db: Session, sections: list, navigation_id: int):
    for section in sections:
        # # path_list에서 path_id를 찾아서 사용
        # matching_path = next((p for p in paths if p.pathidx == section["pointIndex"]), None)
        
        # if not matching_path:
        #     print(f"⚠️  Path not found for pointIndex={section['pointIndex']}")
        #     continue

        if section['pointIndex'] is None:
            print('pointidx is not exist')

        db.add(RoadSection(
            navigation_id=navigation_id,
            name=section['name'],
            distance=section['distance'],
            pointidx=section['pointIndex'],
            pointcount=section['pointCount'],
            speed=section['speed'],
            congestion=CONGESTION_MAP.get(section["congestion"], "정보 없음")
        ))
