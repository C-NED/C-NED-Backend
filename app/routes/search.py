# from fastapi import APIRouter, Depends
# from app.models.search import RouteSearchResponse
# import urllib.parse
# from app.services.naver_api import get_location_search

# router = APIRouter(prefix="/navigation", tags=["Navigation"])

# #키워드로 지역 선택하기

# @router.get("/route_guide", response_model=RouteSearchResponse)
# def pick_location_search(keyword : str):
#     print(keyword)
#     # keyword = urllib.parse.unquote(keyword)
#     """출발지와 도착지 간의 경로 탐색"""
#     return get_location_search(keyword)
