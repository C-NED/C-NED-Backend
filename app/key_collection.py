import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

NAVERCLOUD_CLIENT_ID = os.getenv("NAVERCLOUD_CLIENT_ID")
NAVERCLOUD_CLIENT_SECRET = os.getenv("NAVERCLOUD_CLIENT_SECRET")
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_ROUTE_API_URL = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
NAVER_SIGNATURE_KEY = os.getenv("NAVER_SIGNATURE_KEY")
NAVER_TIMESTAMP = os.getenv("NAVER_TIMESTAMP")