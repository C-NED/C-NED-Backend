from fastapi import FastAPI, Path, Query
import requests
from fastapi.responses import RedirectResponse
from app.routes.navigation import router as navigation
from app.routes.location import router as location
from app.routes.search import router as search
from app.routes.gps import router as gps
from app.routes.traffics import router as traffics
from app.routes.alert import router as alert

app = FastAPI(
    title="🚀Doby API",
    description="""
    이 API는 네이버 지도 API를 사용하여 기본적인 네이게이션 기능을 제공하며, AI 카메라 분석을 통하여 도로 위 장애물을 감지하고 이를 반영한 맞춤형 주행 경로를 제공하는 것을 목적으로 합니다.

    대표적 기능은 아래와 같습니다.

    🔹 기능 목록
    - 🚗 최적 경로 탐색 (`/navigation/route_guide`)
    - 📍  선택한 지역의 경도 및 위도 반환(`/navigation/locationpick/coordinate`)
    - 🔥 선택한 좌표의 주소 반환(`/navigation/locationpick/address`)
    - ✅ 키워드 서치 시 장소 주소 반환(`/navigation/locationpick/search`)
    - 🌐 IP를 기반으로 GPS 위치 반환(`/navigation/gps`)
   """,
    version="1.0.0",
)

@app.get("/", include_in_schema=False)
async def root():
    # /docs 경로로 리디렉션
    return RedirectResponse(url="/docs")

app.include_router(navigation,prefix="/navigation",tags=["Navigation"])
app.include_router(location,prefix="/navigation",tags=["Navigation"])
app.include_router(search,prefix="/navigation",tags=["Navigation"])
app.include_router(gps,prefix="/navigation",tags=["Navigation"])

app.include_router(traffics,prefix="/navigation",tags=["Road"])
app.include_router(alert,prefix="/navigation",tags=["Road"])