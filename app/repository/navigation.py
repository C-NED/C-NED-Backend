from sqlalchemy.orm import Session
from app.models.db_model.navigation import Navigation
from app.models.db_model.path import Path
from app.models.db_model.road_section import RoadSection
from app.models.traffic_model.route import Route  # Pydantic 기반 입력값 schema
from datetime import datetime, timedelta
from app.models.db_model.types.point import Point
from shapely.geometry import Point as ShapelyPoint

def save_navigation(db: Session ,summary:list,option:str,principal_type: str, principal_id: int) -> Navigation:

    start = summary['start']['location']
    goal = summary['goal']['location']

    start_shapely = ShapelyPoint(start[1],start[0])
    end_shapely = ShapelyPoint(goal[1],goal[0])

    navigation = Navigation(
        principal_type=principal_type,
        principal_id=principal_id,
        start_loc=start_shapely,
        end_loc=end_shapely,
        arrival_time=datetime.fromisoformat(summary['departureTime']) + timedelta(milliseconds=summary['duration']),
        road_option=f'{option}',
        total_distance=summary['distance'],
        total_time=summary['duration'],
        fuelprice=summary['fuelPrice'],
        taxifare=summary['taxiFare'],
        tollfare=summary['tollFare'],
    )

    db.add(navigation)
    db.flush()  # navigation_id 확보

    return navigation
