from fastapi import APIRouter, Depends,Query
# from app.models.traffics import TrafficResponse
from app.models.traffic_model.default import Model404,Model422
from app.services.road_api import find_outbreaks,find_caution_sections,find_dangerous_incident,find_VSL
from typing import Optional
from app.models.traffic_model.alert import CautionInput, OutbreakResponse,CautionsResponseModel,DangerousIncidentResponse,VSLResponseModel

router = APIRouter()

#선택한 도로의 돌발 사고 정보 반환

@router.get("""/outbreaks""",
         summary="돌발상황 API",
         description="특정 도로의 돌발 사고 정보를 반환하는 API입니다.",
         responses={200:{"description":"요청 성공","model":OutbreakResponse},404:{"description":"검색 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})

def get_outbreaks(type : str = Query(default="all",description="all: 전체 / ex: 고속도로 / its: 국도 / loc: 지방도 / sgg: 시군도 / etc: 기타") ,
                 eventType : str = Query(default="all",description="all: 전체 / cor: 공사 / acc: 교통사고 / wea: 기상 / ete: 기타돌발 / dis: 재난 / etc: 기타"),
                 minX : Optional[str] = Query(default=None,example=126.800000,description="최소 경도 영역 도로 정보(all) 또는 이벤트 유형(all)의 경우, 사용 가능"),
                 maxX : Optional[str] = Query(default=None,example=127.890000,description="최대 경도 영역 도로 정보(all) 또는 이벤트 유형(all)의 경우, 사용 가능"),
                 minY : Optional[str] = Query(default=None,example=34.900000,description="최소 위도 영역 도로 정보(all) 또는 이벤트 유형(all)의 경우, 사용 가능"),
                 maxY : Optional[str] = Query(default=None,example=35.100000,description="최대 위도 영역 도로 정보(all) 또는 이벤트 유형(all)의 경우, 사용 가능")
):  
    return find_outbreaks(type,eventType,minX,minY,maxX,maxY)


#주의 운전 구간 정보 반환

@router.get("""/cautions""",
         summary="주의운전구간 API",
         description="특정 도로의 주의운전구간 정보를 반환하는 API입니다.",
         responses={200:{"description":"요청 성공","model":CautionsResponseModel},404:{"description":"검색 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})

def get_caution_sections(start_loc : list[float,float] = Query(default=None,example=[126.800000,34.900000],description="시작 위치 좌표"),
                         end_loc : list[float,float] = Query(default=None,example=[127.890000,35.100000],description="끝나는 위치 좌표")):
                        
    return find_caution_sections(start_loc,end_loc)


#위험물질 운송차량 사고정보 반환

@router.get("""/dangerous_incident""",
         summary="위험물질 운송차량 사고정보 API",
         description="위험물질 운송차량 사고 정보를 반환하는 API입니다.",
         responses={200:{"description":"요청 성공","model":DangerousIncidentResponse},404:{"description":"검색 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})

def get_dangerous_incident():
    return find_dangerous_incident()

#가변속도표지제한정보 반환
@router.get("""/vsl""",
         summary="가변속도표지제한정보 API",
         description="가변속도표지제한정보를 반환하는 API입니다.",
         responses={200:{"description":"요청 성공","model":VSLResponseModel},404:{"description":"검색 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})
def get_VSL():
    return find_VSL()