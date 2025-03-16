import requests
from app.config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET,NAVER_SIGNATURE_KEY,NAVER_TIMESTAMP
import urllib.parse
from fastapi import Query

NAVER_ROUTE_API_URL = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"

def get_navigation_route(start_lat, start_lng, end_lat, end_lng):
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_CLIENT_SECRET
    }
    
    params = {
        "start": f"{start_lng},{start_lat}",
        "goal": f"{end_lng},{end_lat}",
        "option": "trafast"
    }
    
    response = requests.get(NAVER_ROUTE_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch route", "status_code": response.status_code}


def get_location_coordinate(query):
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_CLIENT_SECRET
    }
    
    params = {
        "query": query
    }
    
    response = requests.get("https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode", headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch location", "status_code": response.status_code}
    
def get_location_address(latitude, longitude):
    coords = f"{longitude},{latitude}"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_CLIENT_SECRET,
        "Accept": "application/json"
    }
    
    params = {
        "coords": coords,
        "output": "json"
    }
    
    response = requests.get("https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        decoded_query = urllib.parse.unquote(data)
        return decoded_query
    else:
        return {"error": "Failed to fetch address", "status_code": response.status_code , "response_text" : response.text}
    

def get_location_search(keyword):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        "Accept": "application/json"
    }
    
    params = {
        "query": f"{keyword}",
        "output": "json"
    }
    
    response = requests.get("https://openapi.naver.com/v1/search/local.json", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        decoded_query = urllib.parse.unquote(data)
        return decoded_query
    else:
        return {"error": "Failed to fetch address", "status_code": response.status_code , "response_text" : response.text}
    
def get_gps_location(ip):
    headers = {
        "x-ncp-iam-access-key": NAVER_CLIENT_ID,
        "x-ncp-apigw-signature-v2": NAVER_SIGNATURE_KEY,
        "x-ncp-apigw-timestamp" : NAVER_TIMESTAMP
    }
    
    params = {
        "ip": f"{ip}",
        "output": "json"
    }

    response = requests.get("https://geolocation.apigw.ntruss.com/geolocation/v2/geoLocation", headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch location", "status_code": response.status_code , "response_text" : response.text}