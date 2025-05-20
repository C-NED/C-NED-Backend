from shapely.geometry import Point as ShapelyPoint
from sqlalchemy.orm import Session
from app.models.db_model.dangerous_incident import DangerousIncident

def save_dincident(db: Session, dincidents: dict,navigation_id:int,principal_type: str, principal_id: int) :
    saved_dincidents = []  # 저장된 caution 객체들을 담을 리스트
   
   # 각 caution 항목을 순회하면서 저장
    for d in dincidents:
   
        try:
            coord = float(d["xcrdnt"]), float(d["ycrdnt"])
            loc = ShapelyPoint(coord)
            # wkt = loc.wkt  # 예: 'LINESTRING (126.1234 37.5678, 126.4567 37.6789)'


            dincident = DangerousIncident(
                navigation_id=navigation_id,
                principal_id=principal_id,
                principal_type=principal_type,
                loc=loc,
                period=d["acdntOccrrncDt"]+d["acdntEndAt"],
            )
            db.add(dincident)
        except Exception as e:
            print(f"❌ dincindet 저장 실패 - period: {d.get('acdntOccrrncDt')} + {d.get('acdntEndAt')}, 에러: {e}")
            print(f"↪️  원본 좌표: xcrdnt={d.get('xcrdnt')} ycrdnt={d.get('ycrdnt')} ")
            continue
        saved_dincidents.append(dincident)  # 저장된 caution 객체를 리스트에 추가

    db.flush()

    return saved_dincidents
