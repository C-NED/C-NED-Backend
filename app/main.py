from fastapi import FastAPI, Path, Query
# from pydantic import BaseModel, Field
import requests
from pydantic import constr
import os
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from app.models.gps import LocationRequest
from app.models.route import Model404, RouteResponse,Model422
from app.models.location import CoLocationResponse,AdLocationResponse
from app.models.search import SearchResponse
from app.models.gps import LocationRequest

# 환경 변수 로드
load_dotenv()

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

# 네이버 API 설정
NAVERCLOUD_CLIENT_ID = os.getenv("NAVERCLOUD_CLIENT_ID")
NAVERCLOUD_CLIENT_SECRET = os.getenv("NAVERCLOUD_CLIENT_SECRET")
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_ROUTE_API_URL = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
NAVER_SIGNATURE_KEY = os.getenv("NAVER_SIGNATURE_KEY")
NAVER_TIMESTAMP = os.getenv("NAVER_TIMESTAMP")

# # Pydantic 모델을 사용하여 IP 검증
# class GpsRequest(BaseModel):
#     ip: str = Field(..., pattern=r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", description="공인 ip 주소 ex)192.168.12.32")

@app.get("""/navigation/route_guide""",
         summary="출발지와 도착지 간의 경로 탐색 API",
         description="출발지와 도착지 간의 최적 경로를 탐색하는 API입니다."
        #  description="출발지,도착지의 위도,경도를 순서대로 넣고 경로 탐색 옵션(trafast,tracomfort,traoptimal,traviodtoll,traavoidcaronly)을 선택하여 경로를 탐색하는 API입니다."
         ,tags=["Navigation"],
         responses ={200:{"description":"경로 탐색 성공","model":RouteResponse},404:{"description":"경로 탐색 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}}
        #  description = "start_lat: 출발지 위도, start_lng: 출발지 경도, end_lat: 도착지 위도, end_lng: 도착지 경도, option: 경로 탐색 옵션(trafast,tracomfort,traoptimal,traviodtoll,traavoidcaronly)",
         )
def get_route(start_lat: float = Query(default=127.14539383300,description="출발지 위도") , start_lng: float = Query(default=37.47309983000,description="출발지 경도"), end_lat: float = Query(default=129.0756416,description="도착지 위도"), end_lng: float = Query(default=35.1795543,description="도착지 경도"), option: str = Query(default="trafast",description="경로 탐색 옵션(trafast(가장 빠른 경로),tracomfort(가장 편한 경로),traoptimal(최적의 경로),traviodtoll(무료 우선),traavoidcaronly(차량 우선))")):
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVERCLOUD_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVERCLOUD_CLIENT_SECRET,
        "X-Naver-Client-App-Id": "com.doby"
    }
    
    params = {
        "start": f"{start_lat},{start_lng}",
        "goal": f"{end_lat},{end_lng}",
        "option": f"{option}"
    }
    
    # option에 trafast,tracomfort,traoptimal,traviodtoll,traavoidcaronly 중 하나 선택

    response = requests.get(NAVER_ROUTE_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("route"):
            return data["route"]
    else:
        return {"error": "Failed to fetch route", "status_code": response.status_code}

@app.get("""/navigation/locationpick/coordinate""",
         summary="선택한 지역의 경도 및 위도 반환 API",
         description="주소를 기반으로 경도 및 위도를 반환하는 API입니다.",
         tags=["Navigation"],
         responses={200:{"description":"주소 반환 성공","model":CoLocationResponse},404:{"description":"주소 반환 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})
def picklocation_co(query : str = Query(default="서울특별시 종로구 사직로 161",description="한글 도로명 주소")):
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVERCLOUD_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVERCLOUD_CLIENT_SECRET,
        "X-Naver-Client-App-Id": "com.doby"
    }
    
    params = {
        "query": f"{query}"
    }
    
    response = requests.get("https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # 📌 필요한 데이터만 추출 (첫 번째 주소 정보)
        if data.get("addresses"):
            address_info = data["addresses"][0]
            return {
                "roadAddress": address_info["roadAddress"],
                "jibunAddress": address_info["jibunAddress"],
                "latitude": address_info["y"],
                "longitude": address_info["x"]
            }
        else:
            return {"error": "No address found"}
    else:
        return {"error": "Failed to fetch location", "status_code": response.status_code}

@app.get("""/navigation/locationpick/address""",
         summary="선택한 좌표 주소 반환 API",
         description="위도와 경도를 기반으로 한글 주소를 반환하는 API입니다.",
         tags=["Navigation"],
         responses={200:{"description":"주소 반환 성공","model":AdLocationResponse},404:{"description":"주소 반환 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})
def picklocation_ad(latitude: str = Query(default=129.0756416,description="위도"), longitude: str = Query(default=35.1795543,description="경도")):
    NAVER_LOCATION_URL = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"

    """
    위도/경도를 입력받아 한글 주소(행정 주소) + POI(주요 지명) 정보를 반환
    :param latitude: 위도 (예: "37.4505")
    :param longitude: 경도 (예: "127.1270")
    :return: {"address": "주소", "place": "주요 장소"}
    """

    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVERCLOUD_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVERCLOUD_CLIENT_SECRET,
        "X-Naver-Client-App-Id": "com.doby"
    }

    # 🔹 1️⃣ Reverse Geocoding API 호출 (주소 변환)

    params = {
        "coords": f"{latitude},{longitude}",
        "output": "json",
    }
    
    response = requests.get(NAVER_LOCATION_URL, headers=headers, params=params)
    
    if response.status_code == 200:
       return response.json()
    else:
        return {"error": "Failed to fetch address", "status_code": response.status_code,"response_text":response.text}
    

@app.get("""/navigation/locationpick/search""",
         summary="장소 검색 API",
         description="키워드를 기반으로 정보를 반환하는 검색 관련 API입니다."
         ,tags=["Navigation"],
         responses={200:{"description":"검색 성공","model":SearchResponse},404:{"description":"검색 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})
def picklocation_search(keyword : str = Query(default="가천대",description="검색할 키워드")):
    
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        "Accept": "application/json"
    }
    
    params = {
        "query": f"{keyword}",
    }

    response = requests.get("https://openapi.naver.com/v1/search/local.json", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get("items"):
            Items = data["items"][0]
            mapx = int(Items["mapx"]) / 10000000
            mapy = int(Items["mapy"]) / 10000000

            return {
                "title" : Items["title"],
                "link" : Items["link"],
                "category" : Items["category"],
                "roadAddress" : Items["roadAddress"],
                "mapx" : str(mapx),
                "mapy" : str(mapy)
            }
    else:
        return {"error": "Failed to fetch location", "status_code": response.status_code}
    
@app.get("""/navigation/gps""",tags=["Navigation"],description="GPS 정보를 반환하는 API입니다.",summary="GPS 정보 반환 API",responses={200:{"description":"GPS 정보 반환 성공","model":LocationRequest},404:{"description":"GPS 정보 반환 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})
async def receive_location(data: LocationRequest):
    return {
        "message": "GPS 데이터 수신 완료",
        "latitude": data.latitude,
        "longitude": data.longitude,
    }