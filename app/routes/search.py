from fastapi import APIRouter, Depends,Query
from app.models.search import SearchResponse
from app.models.default import Model404,Model422
from app.services.naver_api import picklocation_search

router = APIRouter()

#키워드로 지역 선택하기

@router.get("""/locationpick/search""",
         summary="장소 검색 API",
         description="키워드를 기반으로 정보를 반환하는 검색 관련 API입니다.",
         responses={200:{"description":"검색 성공","model":SearchResponse},404:{"description":"검색 실패","model":Model404},422:{"description":"입력값 오류","model":Model422}})
# def picklocation_search(keyword : str = Query(default="가천대",description="검색할 키워드")):
    
#     headers = {
#         "X-Naver-Client-Id": NAVER_CLIENT_ID,
#         "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
#         "Accept": "application/json"
#     }
    
#     params = {
#         "query": f"{keyword}",
#     }

#     response = requests.get("https://openapi.naver.com/v1/search/local.json", headers=headers, params=params)
    
#     if response.status_code == 200:
#         data = response.json()
        
#         if data.get("items"):
#             Items = data["items"][0]
#             mapx = int(Items["mapx"]) / 10000000
#             mapy = int(Items["mapy"]) / 10000000

#             return {
#                 "title" : Items["title"],
#                 "link" : Items["link"],
#                 "category" : Items["category"],
#                 "roadAddress" : Items["roadAddress"],
#                 "mapx" : str(mapx),
#                 "mapy" : str(mapy)
#             }
#     else:
#         return {"error": "Failed to fetch location", "status_code": response.status_code}
def get_search(keyword : str = Query(default="가천대",description="검색할 키워드")):
    """
    키워드를 입력받아 해당 키워드의 정보를 반환
    :param keyword: 검색할 키워드 (예: "가천대")
    :return: {"title": "제목", "link": "링크", "category": "카테고리", "roadAddress": "도로명 주소", "mapx": "위도", "mapy": "경도"}
    """
    return picklocation_search(keyword)