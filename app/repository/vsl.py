from shapely.geometry import Point as ShapelyPoint
from geoalchemy2.shape import from_shape
from sqlalchemy.orm import Session
from app.models.db_model.vsl import Vsl

def save_vsl(db: Session, vsls: dict, navigation_id: int, principal_type: str, principal_id: int):
    saved_vsls = []

    for v in vsls:
        try:
            coord = float(v["coordX"]) , float(v["coordY"])
            loc = from_shape(ShapelyPoint(coord), srid=4326)

            vsl = Vsl(
                navigation_id=navigation_id,
                principal_id=principal_id,
                principal_type=principal_type,
                vsl_name=v["vslName"],
                loc=loc,
                registedDate=v["registedDate"],
                road_no=v["roadNo"],
                default_speed_limit=int(v["defLmtSpeed"]),
                cur_speed_limit=int(v["limitSpeed"]),
            )
            db.add(vsl)
            saved_vsls.append(vsl)

        except Exception as e:
            print(f"❌ vsl 저장 실패 - 에러: {e}")
            print(f"↪️  원본 좌표: coordX={v.get('coordX')} coordY={v.get('coordY')}")
            continue

    db.flush()
    return saved_vsls
