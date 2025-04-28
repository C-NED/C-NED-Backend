from fastapi import APIRouter, Depends,Query
from app.models.traffic_model.gps import LocationRequest
from app.services.naver_api import receive_location
from app.models.traffic_model.default import Model404,Model422

router = APIRouter()

@router.get("""/gps""",description="GPS 정보를 반환하는 API입니다.",summary="GPS 정보 반환 API",responses={200:{"description":"GPS 정보 반환 성공","model":LocationRequest},404:{"description":"GPS 정보 반환 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})
async def get_location(data: LocationRequest):
    return receive_location(data)