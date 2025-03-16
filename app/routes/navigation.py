from fastapi import APIRouter, Depends,Query
from app.services.naver_api import get_navigation_route
from app.services.naver_api import get_location_coordinate
from app.services.naver_api import get_location_address
from app.models.location import CoLocationResponse,AdLocationResponse
from app.models.search import RouteSearchResponse
from app.services.naver_api import get_location_search
from app.models.route import RouteResponse
import urllib.parse


#출발지와 도착지 간의 최적 경로 탐색

router = APIRouter()

@router.get("/route_guide", response_model=RouteResponse)
def get_route(start_lat: float, start_lng: float, end_lat: float, end_lng: float,option: str):
    """출발지와 도착지 간의 경로 탐색"""
    return get_navigation_route(start_lat, start_lng, end_lat, end_lng,option)


# #위치 선택 시 좌표 및 주소 반환

# @router.get("locationpick/coordinate",response_model=CoLocationResponse)
# def picklocation_coordinate(query : str = Query(...,description="위치를 입력하세요")):
#     # 선택한 위치의 좌표 반환
#     decoded_query = urllib.parse.unquote(query)
#     # 한글 주소가 깨지므로 다시 디코드하여 전달
#     return get_location_coordinate(decoded_query)

# @router.get("locationpick/address",response_model=AdLocationResponse)
# def picklocation_address(latitude: str = Query(...,description="위도를 입력하세요"),
#                          longitude: str = Query(...,description="경도를 입력하세요")):
#     return get_location_address(latitude,longitude)


# @router.get("/route_guide", response_model=RouteSearchResponse)
# def pick_location_search(keyword : str):
#     """출발지와 도착지 간의 경로 탐색"""
#     return get_location_search(keyword)
