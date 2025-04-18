from shapely.geometry import Point as ShapelyPoint 
from sqlalchemy.orm import Session
from app.models.db_model.outbreak import Outbreak

def save_outbreak(db: Session, outbreaks: dict,navigation_id:int,principal_type: str, principal_id: int) :
    saved_outbreaks = []  # 저장된 caution 객체들을 담을 리스트
   
   # 각 outbreak 항목을 순회하면서 저장
    for o in outbreaks:
   
        try:
            coord = float(o["coordX"]), float(o["coordY"])
            loc = ShapelyPoint(coord)
            wkt = loc.wkt  # 예: 'LINESTRING (126.1234 37.5678, 126.4567 37.6789)'


            outbreak = Outbreak(
                navigation_id=navigation_id,
                principal_id=principal_id,
                principal_type=principal_type,
                event_type=o["eventType"]+o["eventDetailType"],
                period=o["startDate"]+o["endDate"],
                road_name=o["roadName"],
                message=o["message"],
                loc=wkt,
                road_no=o["roadNo"],
            )
            db.add(outbreak)
        except Exception as e:
            print(f"❌ outbreak 저장 실패 - period: {o.get('startDate')} + {o.get('endDate')}, 에러: {e}")
            print(f"↪️  원본 좌표: xcrdnt={o.get('coordX')} ycrdnt={o.get('coordY')} ")
            continue
        saved_outbreaks.append(outbreak)  # 저장된 caution 객체를 리스트에 추가

    db.flush()

    return saved_outbreaks