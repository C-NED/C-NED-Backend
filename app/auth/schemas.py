from typing import Any, List, Union
from pydantic import BaseModel

#refresh_token 발급 request model
class RefreshTokenRequest(BaseModel):
    refresh_token: str

class model404(BaseModel):
    detail : str

class model401(BaseModel):
    detail : str

class ErrorContext(BaseModel):
    error: str

class ErrorDetail(BaseModel):
    type: str
    loc: List[Union[str, int]]
    msg: str
    input: Any
    ctx: ErrorContext


class model422(BaseModel):
    detail: List[ErrorDetail]


class RefreshtokenResponse(BaseModel):
    detail: str

class LoginResponse(BaseModel):
    access_token : str

class Login422ErrorDetail(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str

class Login422ErrorResponse(BaseModel):
    detail: List[Login422ErrorDetail]