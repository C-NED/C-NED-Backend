from sqlalchemy.orm import Session
from app.models.db_model.navigation import Navigation
from app.models.db_model.path import Path
from app.models.db_model.road_section import RoadSection
from app.models.traffic_model.route import Route  # Pydantic 기반 입력값 schema
from datetime import datetime, timedelta
from app.models.db_model.types.point import Point
from shapely.geometry import Point as ShapelyPoint


def save_navigation(db: Session, data: dict, principal_type: str, principal_id: int) -> Navigation:
    if(data):
        print("data exist")

    summary = data["trafast"][0]['summary']
    start = summary['start']['location']
    goal = summary['goal']['location']

    start_shapely = ShapelyPoint(start[0], start[1])
    end_shapely = ShapelyPoint(goal[0], goal[1])

    navigation = Navigation(
        principal_type=principal_type,
        principal_id=principal_id,
        start_loc=start_shapely,
        end_loc=end_shapely,
        arrival_time=datetime.fromisoformat(summary['departureTime']) + timedelta(milliseconds=summary['duration']),
        road_option='trafast',
        total_distance=summary['distance'],
        total_time=summary['duration'],
        fuelprice=summary['fuelPrice'],
        taxifare=summary['taxiFare'],
        tollfare=summary['tollFare'],
    )

    db.add(navigation)
    db.flush()  # navigation_id 확보

    return navigation
