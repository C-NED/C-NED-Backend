from fastapi import APIRouter, Depends,Query
from app.models.gps import GPSResponse

router = APIRouter()

@router.get("/gps", response_model=GPSResponse)
def get_gps(ip : str = Query(...,description="ip를 입력하세요")):
    return get_gps_location(ip)