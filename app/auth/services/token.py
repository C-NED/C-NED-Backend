# auth/services/token.py

from datetime import datetime, timedelta
import json
from jose import jwt
from sqlalchemy.orm import Session
from app.models.db_model.refresh_token import RefreshToken
import redis
from app.key_collection import SECRET_KEY,ALGORITHM,ACCESS_EXPIRE_MINUTES
import secrets
from fastapi import HTTPException, status
import hashlib
from app.key_collection import REDIS_URL

# Redis 연결
r = redis.from_url(
    REDIS_URL,
    decode_responses=True  # string 자동 디코딩
)

try:
    pong = r.ping()
    print("Redis 연결 성공!" if pong else "Redis 연결 실패!")
except Exception as e:
    print("Redis 연결 오류:", e)


def create_access_token(db: Session, data: dict, expires_delta: timedelta = None, secret_key: str = None):
    if secret_key is None:
        secret_key = secrets.token_urlsafe(32)
        
    to_encode = data.copy()
    
    # ADMIN인 경우 admin_type 조회 후 principal_type 덮어쓰기
    if data.get("principal_type") == "ADMIN":
        admin = db.query(AdminModel).filter(AdminModel.id == data["principal_id"]).first()
        if admin and hasattr(admin, "admin_type") and admin.admin_type:
            to_encode["principal_type"] = admin.admin_type  # ex: "road_admin", "service_admin"
    
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    
    r.setex(
        encoded_jwt,
        timedelta(minutes=ACCESS_EXPIRE_MINUTES),
        json.dumps({
            "principal_id": to_encode["principal_id"],
            "principal_type": to_encode["principal_type"],
            "exp": expire.isoformat()
        })
    )    
    
    return encoded_jwt


def verify_access_token(token: str):
    role = r.get(token)
    if not role:
        raise HTTPException(status_code=401, detail="Access token expired or revoked")
    return role.decode()

def is_blacklisted(token: str):
    return r.exists(f"blacklist:{token}")

def blacklist_token(token: str):
    ttl = r.ttl(token)
    if ttl > 0:
        r.setex(f"blacklist:{token}", ttl, "true")


def create_refresh_token(db: Session, p_id: int, p_type: str):

    # type에 따라 기한 다르게 설정
    if p_type == "USER":
        expires_in = timedelta(days=15)  # 일반 유저는 15일
    elif p_type =="ADMIN":
        expires_in = timedelta(days=30)  # 관리자(road_admin, service_admin)는 30일
    else:
        expires_in = timedelta(days=15)  # 기본값은 15일

    payload = {
        "principal_id": p_id,
        "principal_type": p_type,
        "exp": datetime.utcnow() + expires_in
    }

    refresh_token_str = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # BINARY(32)이므로 SHA-256 해시
    hashed_token = hashlib.sha256(refresh_token_str.encode("utf-8")).digest()

    db_token = RefreshToken(principal_id=p_id,principal_type=p_type,refresh_token=hashed_token, expires_at=datetime.utcnow() + expires_in)
    db.add(db_token)
    db.commit()
    return refresh_token_str, hashed_token


def manage_refresh_token(db: Session, p_id: int, p_type: str):
    # 기존 리프레시 토큰 확인
    existing_token = db.query(RefreshToken).filter_by(principal_id=p_id, principal_type=p_type).first()

    #유효한 경우 내버려둠
    if existing_token:
        if existing_token.expires_at > datetime.utcnow():
            raise HTTPException(status_code=400, detail="Token is still valid.")
    #만료된 경우 삭제
        else:
            db.delete(existing_token)
            db.commit()
    

    # 토큰 만료된 경우 새로운 토큰 발급 및 새로운 secret_key 생성
    refresh_token, secret_key = create_refresh_token(db, p_id, p_type)
    
    # 새 secret_key로 access_token 발급
    new_access_token = create_access_token({"principal_id": p_id, "principal_type": p_type}, secret_key=secret_key)

    return {"access_token": new_access_token, "refresh_token": refresh_token}

