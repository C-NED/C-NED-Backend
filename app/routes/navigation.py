from fastapi import APIRouter, Depends,Query
from requests import Session
from app.models.traffic_model.route import RouteGuideInput, RouteResponse
from app.repository.dangerous_incident import save_dincident
from app.repository.outbreak import save_outbreak
from app.repository.vsl import save_vsl
from app.services.naver_api import get_route
from app.models.traffic_model.default import Model404,Model422
from app.database import get_db
from app.repository.navigation import save_navigation
from app.repository.path import save_paths
from app.repository.road_section import save_road_sections
from app.repository.guide import save_guide
from app.models.traffic_model.alert import CautionInput
from app.repository.caution import save_caution
from app.services.road_api import find_VSL, find_caution_sections, find_dangerous_incident, find_outbreaks

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
def make_route_guide(start: list = Query(default={127.14539383300,37.47309983},description="출발지 경도,위도"),
                     goal: list = Query(default={129.0756416,35.1795543},description="도착지 경도,위도"),
                     road_option: str = Query(default="trafast",description="경로 탐색 옵션(trafast(가장 빠른 경로),tracomfort(가장 편한 경로),traoptimal(최적의 경로),traviodtoll(무료 우선),traavoidcaronly(차량 우선))")
                     ):
    return get_route(start,goal,road_option)

def create_caution_auto(navigation_id :str, start:list ,goal:list,ptype:str,pid:int,db: Session = Depends(get_db)):
    # 1. Road API 호출 (find_caution 로직)
    data = find_caution_sections(start,goal)
    
    # 2. Navigation 저장
        # data["items"]가 리스트 형태인지 확인
    if isinstance(data["items"], list):
        # caution 저장
        caution = save_caution(db, data["items"], navigation_id, ptype, pid)
    else:
        raise ValueError("data['items'] should be a list but got {}".format(type(data["items"])))


    db.commit()
    return {"saved_cautions_count": len(caution)}

def create_dincident_auto(navigation_id:str,ptype:str,pid:int,db: Session = Depends(get_db)):
    # 1. Road API 호출 (find_dincident 로직)
    data = find_dangerous_incident()
    dincident = save_dincident(db, data["items"], navigation_id, ptype, pid)
    
    db.commit()
    return {"saved_dincidents_count": len(dincident)}

def create_outbreak_auto(start:list,goal:list,navigation_id:str,ptype:str,pid:int,db: Session = Depends(get_db)):
    # 1. Road API 호출 (find_outbreak 로직)
    data = find_outbreaks(start,goal)
    outbreak = save_outbreak(db, data["items"], navigation_id, ptype, pid)
    
    db.commit()
    return {"saved_outbreaks_count": len(outbreak)}

def create_vsl_auto(navigation_id:str,ptype:str,pid:int,db: Session = Depends(get_db)):
    # 1. Road API 호출(find_vsl)
    data = find_VSL()
    vsl = save_vsl(db,data["items"],navigation_id,ptype,pid)

    db.commit()
    return {"saved_vsls_count":len(vsl)}

@router.post("/create")
def create_navigation_auto(payload: RouteGuideInput, db: Session = Depends(get_db)):
    # 1. Naver API 호출 (route_guide 로직)
    data = get_route(payload.start,payload.goal,payload.road_option)

    if payload.road_option not in data:
        raise HTTPException(status_code=400, detail=f"Invalid road option: {payload.road_option}")

    summary = option_data[0].get('summary')
    if not summary:
        raise HTTPException(status_code=400, detail="경로 응답에 summary 없음")
    
    # 2. Navigation 저장
    navigation = save_navigation(db,summary,payload.road_option, principal_type='USER', principal_id=1)

    # # 3. Path + Section 저장
    save_paths(db, data[f"{payload.road_option}"][0]['path'], navigation.navigation_id)
    save_road_sections(db, data[f"{payload.road_option}"][0]['section'], navigation.navigation_id)
    save_guide(db, data[f"{payload.road_option}"][0]['guide'], navigation.navigation_id)

    # # 4. caution 저장
    caution = create_caution_auto(
        navigation_id=navigation.navigation_id,
        start=list(payload.start),
        goal=list(payload.goal),
        ptype=navigation.principal_type,
        pid=navigation.principal_id,
        db=db
    )

    # 5. dincident 저장
    dincident = create_dincident_auto(
        navigation_id=navigation.navigation_id,
        ptype=navigation.principal_type,
        pid=navigation.principal_id,
        db=db
    )

    # 6. outbreak 저장
    outbreak = create_outbreak_auto(
        start=list(payload.start),
        goal=list(payload.goal),
        navigation_id=navigation.navigation_id,
        ptype=navigation.principal_type,
        pid=navigation.principal_id,
        db=db
    )

    #7. vsl 저장
    vsl = create_vsl_auto(
        navigation_id=navigation.navigation_id,
        ptype=navigation.principal_type,
        pid=navigation.principal_id,
        db=db
    )

    db.commit()
    # return {"navigation_id": navigation.navigation_id, "saved_cautions_count": caution["saved_cautions_count"] , "saved_dincidents_count": dincident["saved_dincidents_count"]}
    return {"navigation_id": navigation.navigation_id, "saved_cautions_count": caution["saved_cautions_count"], "saved_dincidents_count": dincident["saved_dincidents_count"], "saved_outbreaks_count": outbreak["saved_outbreaks_count"], "saved_vsls_count": vsl["saved_vsls_count"]}
