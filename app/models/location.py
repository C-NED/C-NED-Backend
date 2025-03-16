from pydantic import BaseModel
from typing import List, Optional

class CoLocationResponse(BaseModel):
    roadAddress: str
    jibunAddress: str
    latitude: str
    longitude: str

class Center(BaseModel):
    crs: str
    x: float
    y: float

class Coords(BaseModel):
    center: Center

class Area(BaseModel):
    name: str
    coords: Coords
    # 일부 지역에는 별칭(alias)이 있으므로 Optional로 처리합니다.
    alias: Optional[str] = None

class Region(BaseModel):
    area0: Area
    area1: Area
    area2: Area
    area3: Area
    area4: Area

class Code(BaseModel):
    id: str
    type: str
    mappingId: str

class Result(BaseModel):
    name: str
    code: Code
    region: Region

class Status(BaseModel):
    code: int
    name: str
    message: str

class AdLocationResponse(BaseModel):
    status: Status
    results: List[Result]