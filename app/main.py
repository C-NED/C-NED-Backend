from fastapi import FastAPI, Path, Query
from inflect import engine
import requests
from fastapi.responses import RedirectResponse
from app.routes.navigation import router as navigation
from app.routes.location import router as location
from app.routes.search import router as search
from app.routes.gps import router as gps
from app.routes.traffics import router as traffics
from app.routes.alert import router as alert
from fastapi.staticfiles import StaticFiles
from app.auth.routes import router as token
from app.models.db_model.base import Base
from app.routes.crud import router as crud

from sqlalchemy.orm import relationship
from app.models.db_model.road_info import RoadInfo
from app.models.db_model.caution import Caution
import time
import pymysql

# # 👇 여기에 모든 모델 import를 명시적으로 추가!
# from app.models.db_model.user import User
# from app.models.db_model.navigation import Navigation
# from app.models.db_model.outbreak import Outbreak
# from app.models.db_model.vsl import Vsl
# from app.models.db_model.caution import Caution
# from app.models.db_model.dangerous_incident import DangerousIncident
# from app.models.db_model.admin import Admin
# from app.models.db_model.favorite_place import FavoritePlace
# from app.models.db_model.refresh_token import RefreshToken

# # 관계만 정의되어 있고, 직접 참조가 없으면 반드시 import 해야 등록됨!

def register_models():
    # 👇 이 안에서 모든 모델 파일 한 번만 import
    import app.models.db_model.user
    import app.models.db_model.navigation
    import app.models.db_model.admin
    import app.models.db_model.outbreak
    import app.models.db_model.vsl
    import app.models.db_model.caution
    import app.models.db_model.dangerous_incident
    import app.models.db_model.favorite_place
    import app.models.db_model.refresh_token
    import app.models.db_model.road_info
    import app.models.db_model.path
    import app.models.db_model.road_section
    import app.models.db_model.types.point
    import app.models.db_model.guide

# 👉 모델 등록 (딱 한 번만!)
register_models()
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🚀CNED API",
    description="""
    이 API는 네이버 지도 API를 사용하여 기본적인 네이게이션 기능을 제공하며, AI 카메라 분석을 통하여 도로 위 장애물을 감지하고 이를 반영한 맞춤형 주행 경로를 제공하는 것을 목적으로 합니다.

    대표적 기능은 아래와 같습니다.

    APP
    ----------------------------------------------------------------------------------------------------------------

    🚗 Navigation API
    목적: 내비게이션 관련 기능을 제공하는 API들로, 경로 탐색, 위치 정보 검색, 좌표 및 주소 반환 등을 처리합니다.

    🛣️ GET /navigation/route_guide:
    출발지와 도착지 간의 경로를 탐색하는 API입니다.
    예시: GET /navigation/route_guide?start=서울&end=부산

    🔄 POST /navigation/create:
    자동으로 네비게이션을 생성하는 API입니다.
    예시: POST /navigation/create { "start": "서울", "end": "부산" }

    📍 GET /navigation/locationpick/coordinate:
    사용자가 선택한 지역의 경도와 위도를 반환하는 API입니다.
    예시: GET /navigation/locationpick/coordinate?location=서울

    🏙️ GET /navigation/locationpick/address:
    사용자가 선택한 장소의 주소를 반환하는 API입니다.
    예시: GET /navigation/locationpick/address?latitude=37.5665&longitude=126.9780

    🔍 GET /navigation/locationpick/search:
    특정 장소를 검색하는 API입니다.
    예시: GET /navigation/locationpick/search?query=서울역

    🚨 Alert API
    목적: 관리자에게 외부 정보를 알리는 API들로, 돌발 상황, 주의 운전 구간, 위험 물질 사고, 가변속도 표지 정보 등을 제공합니다.

    💥 GET /alert/outbreaks:
    돌발상황(예: 사고, 재해 등)을 알리는 API입니다.
    예시: GET /alert/outbreaks

    ⚠️ GET /alert/cautions:
    운전자가 주의해야 할 구간(예: 공사 구간, 사고 다발 지역 등)을 알리는 API입니다.
    예시: GET /alert/cautions

    ☠️ GET /alert/dangerous_incident:
    위험물질 운송과 관련된 사고 정보를 알리는 API입니다.
    예시: GET /alert/dangerous_incident

    📉 GET /alert/vsl:
    가변속도 표지판 정보를 제공하는 API입니다.
    예시: GET /alert/vsl

    ----------------------------------------------------------------------------------------------------------------
    
    APP/WEB 공통
    ----------------------------------------------------------------------------------------------------------------

    🔑 Auth API
    목적: 사용자 인증과 인가를 위한 API로, 로그인, 로그아웃, 토큰 발행 및 갱신, 사용자 정보 조회 등을 처리합니다.

    🖊️ POST /auth/login:
    사용자가 로그인하는 API입니다.
    예시: POST /auth/login { "username": "user", "password": "pass" }

    🚪 POST /auth/logout:
    사용자가 로그아웃하는 API입니다.
    예시: POST /auth/logout

    🟢 GET /auth/access_token/status:
    현재 발급된 액세스 토큰의 상태를 조회하는 API입니다.
    예시: GET /auth/access_token/status

    🔄 GET /auth/refresh_token/return_type_info:
    리프레시 토큰으로 사용자의 정보를 조회하는 API입니다.
    예시: GET /auth/refresh_token/return_type_info

    🆕 POST /auth/token:
    액세스 토큰을 발급하는 API입니다.
    예시: POST /auth/token

    ✔️ POST /auth/access_token/verify:
    발급된 액세스 토큰의 유효성을 확인하는 API입니다.
    예시: POST /auth/access_token/verify { "token": "your_token_here" }

   """,
    version="1.2.0",
    swagger_ui_parameters={"customCssUrl": "/static/docCustom.css"},  # Ensure this URL is correct
)

@app.get("/",include_in_schema=False)
async def root():
    # /docs 경로로 리디렉션
    return RedirectResponse(url="/docs")

@app.get("/health",include_in_schema=False)
async def health():
    return {"status": "ok"}

@app.get("/ping",include_in_schema=False)
async def ping_redis():
    await r.set("key", "value")
    val = await r.get("key")
    return {"key": val}

# def wait_for_mariadb():
#     for i in range(10):
#         try:
#             conn = pymysql.connect(
#                 MARIADB_URL=os.getenv("MARIADB_URL"),
#             )
#             conn.close()
#             print("✅ MariaDB 연결 성공")
#             return
#         except Exception as e:
#             print(f"⏳ MariaDB 대기 중... ({i+1}/10)")
#             time.sleep(3)
#     raise Exception("❌ MariaDB 연결 실패")

# # main.py 초기화 코드 상단에 삽입
# wait_for_mariadb()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(navigation,prefix="/navigation",tags=["navigation"])
app.include_router(location,prefix="/navigation",tags=["navigation"])
app.include_router(search,prefix="/navigation",tags=["navigation"])
# app.include_router(gps,prefix="/navigation",tags=["navigation"])

# app.include_router(traffics,prefix="/alert",tags=["Alert"])
app.include_router(alert,prefix="/alert",tags=["Alert"])
app.include_router(token,prefix="/auth",tags=["auth"])
app.include_router(crud,prefix="/crud",tags=["CRUD"])

from app.models.db_model.base import Base

# print("🔍 현재 SQLAlchemy에 등록된 모델 클래스:")
# for mapper in Base.registry.mappers:
#     print(f" - {mapper.class_.__name__}")

# print("🔍 관계 매핑 확인")
# for mapper in Base.registry.mappers:
#     cls = mapper.class_
#     print(f"[{cls.__name__}] 관계:")
#     for rel in mapper.relationships:
#         print(f" - {rel.key} -> {rel.mapper.class_.__name__}")

