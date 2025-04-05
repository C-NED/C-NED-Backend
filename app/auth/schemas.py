from pydantic import BaseModel

#refresh_token 발급 request model
class RefreshTokenRequest(BaseModel):
    refresh_token: str
