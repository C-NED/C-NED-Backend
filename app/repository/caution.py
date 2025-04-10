from shapely import LineString
from sqlalchemy.orm import Session
from app.models.db_model.caution import Caution

def save_caution(db: Session, cautions: dict,navigation_id:int,principal_type: str, principal_id: int) :
    saved_cautions = []  # 저장된 caution 객체들을 담을 리스트
   
   # 각 caution 항목을 순회하면서 저장
    for c in cautions:
   
        # 시작 ~ 종료 구간 좌표를 리스트로 묶기
        coords = [
            (float(c["startX"]), float(c["startY"])),
            (float(c["revX"]), float(c["revY"]))
        ]

        # LineString 객체로 변환
        loc = LineString(coords)
        
        caution = Caution(
            navigation=navigation_id,
            principal_id=principal_id,
            principal_type=principal_type,
            message=c["message"],
            loc=loc,
            route_no=c["routeNo"],
            route_name=c["reRrouteName"]
        )

        db.add(caution)
        saved_cautions.append(caution)  # 저장된 caution 객체를 리스트에 추가

    db.flush()

    return saved_cautions
