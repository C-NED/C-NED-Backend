# auth/services/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.services.token import create_access_token, create_refresh_token,manage_refresh_token
from model import User
from app.key_collection import SECRET_KEY,ALGORITHM,ACCESS_EXPIRE_MINUTES
from model import RefreshToken
from fastapi import HTTPException, status
from jose import jwt
from app.database import get_db
from app.auth.schemas import RefreshTokenRequest
import hashlib

router = APIRouter()

@router.post("/login")
def login_user(user_id: int, type: str, db: Session = Depends(get_db)):
    access_token = create_access_token({"user_id": user_id, "role": type})
    refresh_token = create_refresh_token(db, user_id, type)
    return {"access_token": access_token, "refresh_token": refresh_token}

# auth/services/routes.py

@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    
    refresh_token = request.refresh_token
    
    hashed_token = hashlib.sha256(refresh_token.encode('utf-8')).digest()
    
    if refresh_token:
        # 기존 리프레시 토큰을 갱신
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        principal_id = payload.get("principal_id")
        principal_type = payload.get("principal_type")

        if not principal_id or not principal_type:
            raise HTTPException(status_code=400, detail="Invalid token payload")

        # DB에서 기존 refresh_token 확인
        token_in_db = db.query(RefreshToken).filter_by(principal_id=principal_id, refresh_token=hashed_token).first()
        if not token_in_db:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # 새로운 access_token 발급
        new_access_token = manage_refresh_token(db, principal_id, principal_type)
        return new_access_token
    
    else:
        # 리프레시 토큰이 없으면 새로 생성
        raise HTTPException(status_code=400, detail="Refresh token is required")