from pydantic import BaseModel,Field
from typing import List, Tuple,Dict, Any
from datetime import datetime


class Summary(BaseModel):
    start: Dict[str, List[float]]
    goal: Dict[str, Any]
    distance: int
    duration: int
    departureTime: datetime
    bbox: List[List[float]]
    tollFare: int
    taxiFare: int
    fuelPrice: int

class Section(BaseModel):
    pointIndex: int
    pointCount: int
    distance: int
    name: str
    congestion: int
    speed: int

class Guide(BaseModel):
    pointIndex: int
    type: int
    instructions: str
    distance: int
    duration: int

class TraoptimalItem(BaseModel):
    summary: Summary
    path: List[List[float]]
    section: List[Section]
    guide: List[Guide]

class Route(BaseModel):
    traoptimal: List[TraoptimalItem]

class RouteResponse(BaseModel):
    code: int = Field(..., example=0)
    message: str = Field(..., example="길찾기를 성공하였습니다.")
    currentDateTime: datetime = Field(..., example="2024-08-27T17:17:21")
    route: Route

class RouteGuideInput(BaseModel):
    start: Tuple[float, float]
    goal: Tuple[float, float]
    road_option: str = "trafast"