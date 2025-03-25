from fastapi import APIRouter, Depends,Query
# from app.models.traffics import TrafficResponse
from app.models.default import Model404,Model422
from app.services.road_api import find_traffics
from app.models.alert import TrafficResponse

router = APIRouter()

#선택한 도로의 실시간 교통정보 반환

@router.get("""/traffics""",
         summary="교통량 API",
         description="특정 도로의 교통량을 반환하는 API입니다.",
         responses={200:{"description":"요청 성공","model":TrafficResponse},404:{"description":"검색 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})

def get_traffics(type : str = Query(default="all",description="all: 전체 / ex: 고속도로 / its: 국도") ,
                roadNo : str = Query(default="0010",description="노선 번호, 도로유형(type)이 all이 아닌 경우 필수 입력"),
                dicType : str = Query(default="all",description="도로 방향(all: 전체 / up: 상행 / down: 하행 / start: 시점 / end: 종점), 도로유형(type)이 all이 아닌 경우 필수 입력"),
                minX : float = Query(default = 126.000,description="최소 경도, 없을 시 timeout이 일어날 수 있음"),
                maxX : float = Query(default = 130.000,description="최대 경도, 없을 시 timeout이 일어날 수 있음"),
                minY : float = Query(default = 34.000,description="최소 위도, 없을 시 timeout이 일어날 수 있음"),
                maxY : float = Query(default = 39.000,description="최대 위도, 없을 시 timeout이 일어날 수 있음"),
                ):
    # """
    # ## 🚦 교통 정보 조회 API  
    # - `type`: 교통 타입 (ex: 고속도로, 국도 등)  
    # - `roadNo`: 도로 번호  
    # - `dicType`: 조회 타입  
    # """
    return find_traffics(type,roadNo,dicType,minX,maxX,minY,maxY)