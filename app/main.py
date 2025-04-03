from fastapi import FastAPI, Path, Query
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

app = FastAPI(
    title="🚀Doby API",
    description="""
    이 API는 네이버 지도 API를 사용하여 기본적인 네이게이션 기능을 제공하며, AI 카메라 분석을 통하여 도로 위 장애물을 감지하고 이를 반영한 맞춤형 주행 경로를 제공하는 것을 목적으로 합니다.

    대표적 기능은 아래와 같습니다.

    
    **주요 기능 목록**
    🔹 최적 경로 탐색: `/navigation/route_guide`  
    🚗 경로를 계산하여 사용자가 최적의 주행 경로를 선택할 수 있도록 지원합니다.

    🔹 선택한 지역의 경도 및 위도 반환: `/navigation/locationpick/coordinate`  
    📍 사용자가 선택한 위치의 정확한 경도 및 위도를 반환합니다.

    🔹 선택한 좌표의 주소 반환: `/navigation/locationpick/address`  
    🔥 사용자가 지정한 좌표에 대한 정확한 주소를 제공합니다.

    🔹 키워드 서치 시 장소 주소 반환: `/navigation/locationpick/search`  
    ✅ 사용자가 입력한 키워드를 기반으로 관련된 장소의 주소를 반환합니다.

    🔹 IP를 기반으로 GPS 위치 반환: `/navigation/gps`  
    🌐 사용자의 IP를 기반으로 GPS 위치를 추적합니다.

    **부가 기능 목록**
    - 🚦 교통량 반환: `/route/traffics`  
    🚗 실시간 교통 상황을 제공하여 최적 경로 선택에 도움을 줍니다.

    - 🚨 돌발상황 반환: `/alert/outbreaks`  
    ⚠️ 도로상의 돌발 상황 정보를 실시간으로 제공합니다.

    - ⚠️ 주의운전구간 반환: `/alert/cautions`  
    🚧 사고 잦은 구간 및 위험 구간에 대한 경고를 제공합니다.

    - ☠️ 위험물질 운송차량 사고 정보 반환: `/alert/dangerous_incident`  
    ☠️ 위험물질 운송 차량의 사고 정보를 실시간으로 알려줍니다.

    - 🚧 가변속도표지제한정보 반환: `/alert/vsl`  
    🚦 도로의 가변속도 제한 표지에 대한 정보를 제공합니다.
   """,
    version="1.0.0",
    swagger_ui_parameters={"customCssUrl": "/static/docCustom.css"},  # Ensure this URL is correct
)

@app.get("/")
async def root():
    # /docs 경로로 리디렉션
    return RedirectResponse(url="/docs")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# app.include_router(navigation,prefix="/navigation",tags=["navigation"])
# app.include_router(location,prefix="/navigation",tags=["navigation"])
# app.include_router(search,prefix="/navigation",tags=["navigation"])
# app.include_router(gps,prefix="/navigation",tags=["navigation"])

# app.include_router(traffics,prefix="/alert",tags=["Alert"])
# app.include_router(alert,prefix="/alert",tags=["Alert"])
app.include_router(token,prefix="/auth",tags=["token"])