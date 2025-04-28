from pydantic import BaseModel
from typing import List, Tuple

class SearchResponse(BaseModel):
    title: str
    link: str
    category: str
    roadAddress: str
    mapx: str
    mapy: str