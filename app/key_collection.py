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

ROAD_API_KEY = os.getenv("ROAD_API_KEY")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_EXPIRE_MINUTES = int(os.getenv("ACCESS_EXPIRE_MINUTES"))

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Redis 설정
REDIS_HOST = os.getenv("REDIS_HOST")  # 기본값은 로컬
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB = int(os.getenv("REDIS_DB"))

# mariadb 설정
MARIADB_HOST = os.getenv("MARIADB_HOST")  # 기본값은 로컬
MARIADB_PORT = int(os.getenv("MARIADB_PORT"))
MARIADB_USER = os.getenv("MARIADB_USER")
MARIADB_DB = os.getenv("MARIADB_DB")
MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD")

# print("ROAD_API_KEY:", os.getenv("ROAD_API_KEY"))
