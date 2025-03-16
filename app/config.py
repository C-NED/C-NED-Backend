import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

NAVERCLOUD_CLIENT_ID = os.getenv("NAVERCLOUD_CLIENT_ID")
NAVERCLOUD_CLIENT_SECRET = os.getenv("NAVERCLOUD_CLIENT_SECRET")


NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")