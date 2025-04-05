from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class OutbreakItem(BaseModel):
    type: str
    eventType: str
    eventDetailType: str
    startDate: str
    coordX: str
    coordY: str
    linkId: str
    roadName: str
    roadNo: str
    roadDrcType: str
    lanesBlockType: Optional[str] = ""
    lanesBlocked: Optional[str] = ""
    message: str
    endDate: Optional[str] = ""

class OutbreakResponse(BaseModel):
    totalCount: int
    items: List[OutbreakItem]


class VSLItem(BaseModel):
    vslId: str
    sectionCode: str
    createdDate: str
    limitSpeed: str
    defLmtSpeed: str
    roadNo: str
    linkId: str
    coordX: float
    coordY: float
    registedDate: str

class VSLResponseModel(BaseModel):
    totalCount: int
    items: List[VSLItem]

class CautionsItem(BaseModel):
    message: str
    stepType: str
    outbrkType: str
    priority: str
    routeName: Optional[str]
    routeNo: str
    roadDrcType: str
    startStdLinkId: str
    startX: str
    startY: str
    revRouteName: str
    revRouteNo: str
    revRoadDrcType: str
    revStdLinkId: str
    revX: str
    revY: str
    occrrncId: Optional[str]

class CautionsResponseModel(BaseModel):
    totalCount: int
    items: List[CautionsItem]


class DangerousIncidentItem(BaseModel):
    streDt: str
    sntcManageNo: str
    acdntOccrrncDt: str
    acdntAt: str
    acdntEndAt: str
    updtDt: date
    ycrdnt: float
    xcrdnt: float

class DangerousIncidentResponse(BaseModel):
    totalcount : int
    items : DangerousIncidentItem

class TrafficItem(BaseModel):
    roadName: str
    roadDrcType: str
    linkNo: str
    linkId: str
    startNodeId: str
    endNodeId: str
    speed: float
    travelTime: float
    createdDate: str

class TrafficResponse(BaseModel):
    totalCount: int
    items: List[TrafficItem]
