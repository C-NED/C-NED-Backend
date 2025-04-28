from shapely import LineString
from sqlalchemy.orm import Session
from app.models.db_model.caution import Caution

def save_caution(db: Session, cautions: dict,navigation_id:int,principal_type: str, principal_id: int) :
    saved_cautions = []  # 저장된 caution 객체들을 담을 리스트
   
   # 각 caution 항목을 순회하면서 저장
    for c in cautions:
   
        try:
            coords = [
                (float(c["startX"]), float(c["startY"])),
                (float(c["revX"]), float(c["revY"]))
            ]
            loc = LineString(coords)
            wkt = loc.wkt  # 예: 'LINESTRING (126.1234 37.5678, 126.4567 37.6789)'


            caution = Caution(
                navigation_id=navigation_id,
                principal_id=principal_id,
                principal_type=principal_type,
                message=c["message"],
                loc=wkt,
                route_no=c["routeNo"],
                route_name=c["revRouteName"]
            )
            db.add(caution)
        except Exception as e:
            print(f"❌ caution 저장 실패 - message: {c.get('message')}, 에러: {e}")
            print(f"↪️  원본 좌표: startX={c.get('startX')} startY={c.get('startY')} revX={c.get('revX')} revY={c.get('revY')}")
            continue
        saved_cautions.append(caution)  # 저장된 caution 객체를 리스트에 추가

    db.flush()

    return saved_cautions
