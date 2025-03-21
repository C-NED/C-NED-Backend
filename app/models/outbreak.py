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

class OutbreakBody(BaseModel):
    totalCount: int
    items: List[OutbreakItem]

class OutbreakHeader(BaseModel):
    resultCode: int
    resultMsg: str

class OutbreakResponse(BaseModel):
    header: OutbreakHeader
    body: OutbreakBody