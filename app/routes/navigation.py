from fastapi import APIRouter, Depends,Query
from requests import Session
from app.models.traffic_model.route import RouteGuideInput, RouteResponse
from app.services.naver_api import get_route
from app.models.traffic_model.default import Model404,Model422
from app.database import get_db
from app.repository.navigation import save_navigation
from app.repository.path import save_paths
from app.repository.road_section import save_road_sections
from app.repository.guide import save_guide

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
def make_route_guide(start: str = Query(default={127.14539383300,37.47309983},description="출발지 경도,위도"),
                     goal: str = Query(default={129.0756416,35.1795543},description="도착지 경도,위도"),
                     road_option: str = Query(default="trafast",description="경로 탐색 옵션(trafast(가장 빠른 경로),tracomfort(가장 편한 경로),traoptimal(최적의 경로),traviodtoll(무료 우선),traavoidcaronly(차량 우선))")
                     ):
    return get_route(start,goal,road_option)


@router.post("/create")
def create_navigation_auto(payload: RouteGuideInput, db: Session = Depends(get_db)):
    # 1. Naver API 호출 (route_guide 로직)
    data = get_route(payload.start,payload.goal,payload.road_option)
    
    # 2. Navigation 저장
    navigation = save_navigation(db, data, principal_type='USER', principal_id=1)

    # 3. Path + Section 저장
    save_paths(db, data['trafast'][0]['path'], navigation.navigation_id)
    save_road_sections(db, data['trafast'][0]['section'], navigation.navigation_id)
    save_guide(db, data['trafast'][0]['guide'], navigation.navigation_id)

    db.commit()
    return {"navigation_id": navigation.navigation_id}
