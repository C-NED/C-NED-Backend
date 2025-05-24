# schemas/crud.py

from typing import Optional, Dict, Any
from pydantic import BaseModel

class CrudRequest(BaseModel):
    table: str
    action: str  # create | read | update | delete
    data: Optional[Dict[str, Any]] = None
    filter: Optional[Dict[str, Any]] = None
