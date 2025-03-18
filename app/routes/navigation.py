from fastapi import APIRouter, Depends,Query
from app.models.route import RouteResponse
from app.services.naver_api import get_route
from app.models.default import Model404,Model422
#출발지와 도착지 간의 최적 경로 탐색


router = APIRouter()

@router.get("""/route_guide""",
         summary="출발지와 도착지 간의 경로 탐색 API",
         description="출발지와 도착지 간의 최적 경로를 탐색하는 API입니다."
        #  description="출발지,도착지의 위도,경도를 순서대로 넣고 경로 탐색 옵션(trafast,tracomfort,traoptimal,traviodtoll,traavoidcaronly)을 선택하여 경로를 탐색하는 API입니다."
         ,
         responses ={200:{"description":"경로 탐색 성공","model":RouteResponse},404:{"description":"경로 탐색 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}}
        #  description = "start_lat: 출발지 위도, start_lng: 출발지 경도, end_lat: 도착지 위도, end_lng: 도착지 경도, option: 경로 탐색 옵션(trafast,tracomfort,traoptimal,traviodtoll,traavoidcaronly)",
         )
# 
def make_route_guide(start_lat: str = Query(default=127.14539383300,description="출발지 위도"),
                     start_lng: str = Query(default=37.47309983000,description="출발지 경도"),
                     end_lat: str = Query(default=129.0756416,description="도착지 위도"),
                     end_lng: str = Query(default=35.1795543,description="도착지 경도"),
                     option: str = Query(default="trafast",description="경로 탐색 옵션(trafast(가장 빠른 경로),tracomfort(가장 편한 경로),traoptimal(최적의 경로),traviodtoll(무료 우선),traavoidcaronly(차량 우선))")
                     ):
    return get_route(start_lat,start_lng,end_lat,end_lng,option)


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
