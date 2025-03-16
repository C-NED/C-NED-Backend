from fastapi import APIRouter, Depends,Query
from app.services.naver_api import get_location_coordinate
from app.services.naver_api import get_location_address
from app.models.location import CoLocationResponse,AdLocationResponse
import urllib.parse

#위치 선택 시 좌표 및 주소 반환
router = APIRouter(prefix="/navigation", tags=["Navigation"])

@router.get("locationpick/coordinate",response_model=CoLocationResponse)
def picklocation_coordinate(query : str):
    # 선택한 위치의 좌표 반환
    decoded_query = urllib.parse.unquote(query)
    # 한글 주소가 깨지므로 다시 디코드하여 전달
    return get_location_coordinate(decoded_query)

@router.get("locationpick/address",response_model=AdLocationResponse)
def picklocation_address(latitude: str,
                         longitude: str):
    return get_location_address(latitude,longitude)
