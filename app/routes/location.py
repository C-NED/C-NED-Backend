from fastapi import APIRouter, Depends,Query
from app.models.location import CoLocationResponse,AdLocationResponse
import urllib.parse
from app.models.default import Model404,Model422
from app.services.naver_api import picklocation_co,picklocation_ad

#위치 선택 시 좌표 및 주소 반환
router = APIRouter()

@router.get("""/locationpick/coordinate""",
         summary="선택한 지역의 경도 및 위도 반환 API",
         description="주소를 기반으로 경도 및 위도를 반환하는 API입니다.",
         responses={200:{"description":"주소 반환 성공","model":CoLocationResponse},404:{"description":"주소 반환 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})
# def picklocation_co(query : str = Query(default="서울특별시 종로구 사직로 161",description="한글 도로명 주소")):
#     headers = {
#         "X-NCP-APIGW-API-KEY-ID": NAVERCLOUD_CLIENT_ID,
#         "X-NCP-APIGW-API-KEY": NAVERCLOUD_CLIENT_SECRET,
#         "X-Naver-Client-App-Id": "com.doby"
#     }
    
#     params = {
#         "query": f"{query}"
#     }
    
#     response = requests.get("https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode", headers=headers, params=params)
    
#     if response.status_code == 200:
#         data = response.json()
        
#         # 📌 필요한 데이터만 추출 (첫 번째 주소 정보)
#         if data.get("addresses"):
#             address_info = data["addresses"][0]
#             return {
#                 "roadAddress": address_info["roadAddress"],
#                 "jibunAddress": address_info["jibunAddress"],
#                 "latitude": address_info["y"],
#                 "longitude": address_info["x"]
#             }
#         else:
#             return {"error": "No address found"}
#     else:
#         return {"error": "Failed to fetch location", "status_code": response.status_code}
def get_location_co(query : str = Query(default="서울특별시 종로구 사직로 161",description="한글 도로명 주소")):
    """
    한글 주소를 입력받아 해당 주소의 좌표(위도/경도)를 반환
    :param query: 한글 주소 (예: "서울특별시 종로구 사직로 161")
    :return: {"roadAddress": "도로명 주소", "jibunAddress": "지번 주소", "latitude": "위도", "longitude": "경도"}
    """
    decoded_query = urllib.parse.unquote(query)
    return picklocation_co(decoded_query)

@router.get("""/locationpick/address""",
         summary="선택한 좌표 주소 반환 API",
         description="위도와 경도를 기반으로 한글 주소를 반환하는 API입니다.",
         responses={200:{"description":"주소 반환 성공","model":AdLocationResponse},404:{"description":"주소 반환 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})
# def picklocation_ad(latitude: str = Query(default=129.0756416,description="위도"), longitude: str = Query(default=35.1795543,description="경도")):
#     NAVER_LOCATION_URL = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"

#     """
#     위도/경도를 입력받아 한글 주소(행정 주소) + POI(주요 지명) 정보를 반환
#     :param latitude: 위도 (예: "37.4505")
#     :param longitude: 경도 (예: "127.1270")
#     :return: {"address": "주소", "place": "주요 장소"}
#     """

#     headers = {
#         "X-NCP-APIGW-API-KEY-ID": NAVERCLOUD_CLIENT_ID,
#         "X-NCP-APIGW-API-KEY": NAVERCLOUD_CLIENT_SECRET,
#         "X-Naver-Client-App-Id": "com.doby"
#     }

#     # 🔹 1️⃣ Reverse Geocoding API 호출 (주소 변환)

#     params = {
#         "coords": f"{latitude},{longitude}",
#         "output": "json",
#     }
    
#     response = requests.get(NAVER_LOCATION_URL, headers=headers, params=params)
    
#     if response.status_code == 200:
#        return response.json()
#     else:
#         return {"error": "Failed to fetch address", "status_code": response.status_code,"response_text":response.text}
    
def get_location_ad(latitude: str = Query(default=129.0756416,description="위도"), longitude: str = Query(default=35.1795543,description="경도")):
    """
    위도/경도를 입력받아 한글 주소(행정 주소) + POI(주요 지명) 정보를 반환
    :param latitude: 위도 (예: "37.4505")
    :param longitude: 경도 (예: "127.1270")
    :return: {"address": "주소", "place": "주요 장소"}
    """
    return picklocation_ad(latitude,longitude)