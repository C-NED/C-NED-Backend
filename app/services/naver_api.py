import requests
import urllib.parse
from fastapi import Query
from app.models.traffic_model.default import Model404,Model422
from app.key_collection import NAVERCLOUD_CLIENT_ID,NAVERCLOUD_CLIENT_SECRET,NAVER_CLIENT_ID,NAVER_CLIENT_SECRET
from fastapi import APIRouter, Depends,Query
from app.models.traffic_model.gps import LocationRequest

NAVER_ROUTE_API_URL = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"

def get_route(start: list[float,float], goal: list[float,float], road_option: str):
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVERCLOUD_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVERCLOUD_CLIENT_SECRET,
        "X-Naver-Client-App-Id": "com.doby"
    }
    
    params = {
        "start": f"{start[0]},{start[1]}",
        "goal": f"{goal[0]},{goal[1]}",
        "option": f"{road_option}"
    }
    
    # option에 trafast,tracomfort,traoptimal,traviodtoll,traavoidcaronly 중 하나 선택

    response = requests.get(NAVER_ROUTE_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("route"):
            return data["route"]
    else:
        return {"error": "Failed to fetch route", "status_code": response.status_code}


def picklocation_co(query : str):
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

def picklocation_ad(latitude: str, longitude: str):
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

def picklocation_search(keyword : str):
    
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
    
    
def receive_location(data: LocationRequest):
    return {
        "message": "GPS 데이터 수신 완료",
        "latitude": data.latitude,
        "longitude": data.longitude,
    }