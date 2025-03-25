import requests
import urllib.parse
from fastapi import Query
from app.models.default import Model404,Model422
from app.key_collection import ROAD_API_KEY
from fastapi import APIRouter, Depends,Query


def find_traffics(type,roadNo,dicType,minX,maxX,minY,maxY):
    # headers  = {
    #     "resultcode" : 0,
    #     "resultmsg" : "정상 처리되었습니다."
    # }
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    params = {
        "apiKey": ROAD_API_KEY,
        "type": f"{type}",
        "routeNo": f"{roadNo}",
        "dicType": f"{dicType}",
        "minX" : f"{minX}",
        "maxX" : f"{maxX}",
        "minY" : f"{minY}",
        "maxY" : f"{maxY}",
        "getType": "json"
    }

    response = requests.get("https://openapi.its.go.kr:9443/trafficInfo",headers=headers, params=params)
    
    # print("요청 URL:", response.url)
    # print("상태 코드:", response.status_code)
    # print("응답:", response.text)


    if response.status_code == 200:
        data = response.json()
        return data
    else : 
        return {"error": "Failed to fetch route", "status_code": response.status_code,"status_msg":response.text}
    

import requests

def find_outbreaks(type, eventType, minX, minY, maxX, maxY):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    params = {
        "apiKey": ROAD_API_KEY,
        "type": type,
        "eventType": eventType,
        "getType": "json"
    }

    # 네 개의 좌표 값이 모두 존재하는 경우만 params에 추가
    if all([minX, minY, maxX, maxY]):
        params.update({
            "minX": minX,
            "minY": minY,
            "maxX": maxX,
            "maxY": maxY
        })

    response = requests.get("https://openapi.its.go.kr:9443/eventInfo", headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("body"):
            body_info = data["body"]
            return {
                "totalCount" : body_info["totalCount"],
                "items" : body_info["items"]
            }
        else:
            return data
    
    else:
        return {
            "error": "Failed to fetch route",
            "status_code": response.status_code,
            "status_msg": response.text
        }

def find_caution_sections(minX, maxX, minY, maxY):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    params = {
        "apiKey": ROAD_API_KEY,
        "minX": f"{minX}",
        "maxX": f"{maxX}",
        "minY": f"{minY}",
        "maxY": f"{maxY}",
        "getType": "json"
    }

    response = requests.get("https://openapi.its.go.kr:9443/posIncidentInfo", headers=headers, params=params)

    print("요청 URL:", response.url)
    print("상태 코드:", response.status_code)
    print("응답:", response.text)

    if response.status_code == 200:
        data = response.json()
        if data.get("body"):
            body_info = data["body"]
            return {
                "totalCount" : body_info["totalCount"],
                "items" : body_info["items"]
            }
        else:
            return data
    
    else:
        return {
            "error": "Failed to fetch route",
            "status_code": response.status_code,
            "status_msg": response.text
        }
    
def find_dangerous_incident():
    params = {
        "apiKey" : ROAD_API_KEY,
        "getType" : "json"
    }

    response = requests.get("https://openapi.its.go.kr:9443/dangerousCarInfo", params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("body"):
            body_info = data["body"]
            return {
                "totalCount" : body_info["totalCount"],
                "items" : body_info["items"]
            }
        else:
            return data
    
    else:
        return {
            "error": "Failed to fetch route",
            "status_code": response.status_code,
            "status_msg": response.text
        }
    
def find_VSL():
    params = {
        "apiKey" : ROAD_API_KEY,
        "getType" : "jSON"
    }

    response = requests.get("https://openapi.its.go.kr:9443/vslInfo",params)

    if response.status_code == 200:
        data = response.json()
        if data.get("body"):
            body_info = data["body"]
            return {
                "totalCount" : body_info["totalCount"],
                "items" : body_info["items"]
            }
        else:
            return data
    else:
        return {
            "error": "Failed to fetch route",
            "status_code": response.status_code,
            "status_msg": response.text
        }