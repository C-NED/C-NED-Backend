# auth/services/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth.services.token import create_access_token, create_refresh_token
from model import User
from app.key_collection import SECRET_KEY,ALGORITHM,ACCESS_EXPIRE_MINUTES
from model import RefreshToken
from fastapi import HTTPException, status


router = APIRouter()

@router.post("/login")
def login_user(user_id: int, type: str, db: Session = Depends(get_db)):
    access_token = create_access_token({"user_id": user_id, "role": type})
    refresh_token = create_refresh_token(db, user_id, type)
    return {"access_token": access_token, "refresh_token": refresh_token}

# auth/services/routes.py

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    from jose import jwt
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    id = payload.get("principal_id")
    type = payload.get("principal_type")

    # DB에 저장된 refresh_token 확인
    token_in_db = db.query(RefreshToken).filter_by(principal_id=id, refresh_token=refresh_token).first()
    if not token_in_db:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # type에 맞는 새로운 access_token 발급
    new_access_token = create_access_token({"principal_id": id, "principal_type": type})
    return {"access_token": new_access_token}
