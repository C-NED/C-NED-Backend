# auth/services/routes.py
from datetime import datetime
import hashlib
from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session
from app.auth.services.token import create_access_token, create_refresh_token,manage_refresh_token, verify_access_token
from app.models.db_model.user import User
from app.key_collection import SECRET_KEY,ALGORITHM,ACCESS_EXPIRE_MINUTES
from app.models.db_model.refresh_token import RefreshToken
from fastapi import HTTPException, status
from jose import JWTError, jwt
from app.database import get_db
from app.auth.schemas import Login422ErrorResponse, LoginResponse, RefreshTokenRequest,RefreshtokenResponse,model401,model404,model422
from app.auth.services.auth_type import get_auth_type
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth.services.token import r
from app.models.db_model.admin import Admin



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/login",
        response_model=LoginResponse,
        responses={
        401: {
            "model": model401,
            "description": "인증 실패",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid credentials"}
                }
            }
        },
        422:{
            "model":Login422ErrorResponse,
            "description":"필드 형식 에러",
            "content": {
                "application/json": {
                    "example": {
                    "detail": [
                        {
                            "loc": ["query", "email"],
                            "msg": "field required",
                            "type": "value_error.missing"
                        }
                    ]
                }
                }
            }
        }
    })
def login_user(email: str, password: str, type: str, db: Session = Depends(get_db)):
    
    # 기존 refresh_token 확인 후 access_token만 새로 발급
    if type == "USER":
        user = db.query(User).filter_by(email=email, password=password).first()
       
        #일단 테스트값의 경우 해시가 아닌 문자열으로 저장하였으므로 나중에 다 해시로 바꾸고 아래 코드로 바꿀 것       
        # 저장된 password는 SHA-256 해시값
        #바꾸고 아래 코드 활성화 완료!
        #편의상 개발 중에는 그냥 위의 코드로 사용하고 나중에는 아래 코드로 바꿀 것(해시를 한 번 더하면 달라져서 어쩔 수 없음)
        # hashed_input = hashlib.sha256(password.encode()).hexdigest()
        # user = db.query(User).filter_by(email=email, password=hashed_input).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials, user not exist")
        principal_id = user.user_id
    elif type == "ADMIN":
        admin = db.query(Admin).filter_by(email=email, password=password).first()
        if not admin:
            raise HTTPException(status_code=401, detail="Invalid credentials, admin not exist")
        principal_id = admin.admin_id
    else:
        raise HTTPException(status_code=400, detail="Invalid user type")

    # 기존 refresh_token 확인
    token_in_db = db.query(RefreshToken).filter_by(
        principal_id=principal_id,
        principal_type=type
    ).first()


    if token_in_db and token_in_db.expires_at > datetime.utcnow():
        # ✅ 유효하면 access_token만 새로 발급
        access_token = create_access_token({
            "principal_id": principal_id,
            "principal_type": type,
        })
        return {
            "access_token": access_token,
            # "refresh_token": token_in_db.refresh_token.hex()  # ← bytes → hex로 반환
        }

    # 만료되었거나 없음 → 새로 발급
    refresh_token, secret_key = create_refresh_token(db, principal_id, type)
    access_token = create_access_token({
        "principal_id": principal_id,
        "principal_type": type,
    }, secret_key=secret_key)

    return {
        "access_token": access_token,
        # "refresh_token": refresh_token
    }

@router.post("/logout")
# TODO: response_model 추가 / 401, 422 응답 정의

def logout(token: str = Depends(oauth2_scheme)):
    r.delete(token)
    return {"message": "Logout successful"}

@router.get("/access_token/status")
# TODO: response_model 추가 / 401, 422 응답 정의

def token_status(token: str = Depends(oauth2_scheme)):
    ttl = r.ttl(token)
    if ttl == -2:
        return {"status": "not found"}
    elif ttl == -1:
        return {"status": "permanent"}
    return {"status": "active", "seconds_left": ttl}


# @router.post("/refresh_token/refresh", responses={200:{"description":"리프레시 토큰 생성 성공","model":RefreshtokenResponse},401:{"description":"Error:Unauthorized","model":model401},404:{"description":"리프레시 토큰 반환 실패","model":model404},422:{"description":"Error: Unprocessable Entity","model":model422}})
# def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    
#     refresh_token = request.refresh_token
    
#     hashed_token = hashlib.sha256(refresh_token.encode('utf-8')).digest()
    
#     if refresh_token:
#         # 기존 리프레시 토큰을 갱신
#         try:
#             payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
#         except jwt.ExpiredSignatureError:
#             raise HTTPException(status_code=401, detail="Refresh token expired")
#         except jwt.JWTError:
#             raise HTTPException(status_code=401, detail="Invalid refresh token")

#         principal_id = payload.get("principal_id")
#         principal_type = payload.get("principal_type")

#         if not principal_id or not principal_type:
#             raise HTTPException(status_code=400, detail="Invalid token payload")

#         # DB에서 기존 refresh_token 확인
#         token_in_db = db.query(RefreshToken).filter_by(principal_id=principal_id, refresh_token=hashed_token).first()
#         if not token_in_db:
#             raise HTTPException(status_code=401, detail="Invalid refresh token")

#         # 새로운 access_token 발급
#         new_access_token = manage_refresh_token(db, principal_id, principal_type)
#         return new_access_token
    
#     else:
#         # 리프레시 토큰이 없으면 새로 생성
#         raise HTTPException(status_code=400, detail="Refresh token is required")
    

@router.get("/refresh_token/return_type_info", summary="리프레시 토큰으로 사용자 정보 조회")
# TODO: response_model 추가 / 401, 422 응답 정의

def get_user_from_refresh_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    
    hashed_token = bytes.fromhex(token)  # ❗ 해시 다시 하지 말고 복원만 하기

    # DB에서 해당 토큰 찾기
    token_obj = db.query(RefreshToken).filter(
        RefreshToken.refresh_token == hashed_token
    ).first()

    if not token_obj:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # principal_type에 따라 분기
    if token_obj.principal_type == "ADMIN":
        data_list = db.query(Admin).all()
        if not data_list:
            raise HTTPException(status_code=404, detail="User not found")
                    
        response = [
        {
            "admin_id": admin.admin_id,
            "admin_type": admin.admin_type,
            "name": admin.name,
            "email": admin.email,
            "profile_img": admin.profile_img
        }
        for admin in data_list
    ]
    else:
        data = db.query(User).filter(User.user_id == token_obj.principal_id).first()
        
        if not data:
            raise HTTPException(status_code=404, detail="User not found")
        
        response = {"user_id":data.user_id,"name":data.name,"email":data.email,"naver_auth":data.naver_auth}
    
    return response
    

@router.post("/token")
#이건 나중에 fast api 문서에서 안 보이게 할 것
def issue_token(form_data: OAuth2PasswordRequestForm = Depends()):
    refresh_token = form_data.username  # 사용자가 여기에 refresh_token 넣는다고 가정
    return {
        "access_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/access_token/verify")
# TODO: response_model 추가 / 401, 422 응답 정의

def verify_access_token(token: str = Depends(oauth2_scheme)):
    role = verify_access_token(token)
    return {"message": f"Hello, {role}"}