# redis_setup.py
import redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 전역에서 쓸 redis 클라이언트
r = redis.from_url(
    REDIS_URL,
    decode_responses=True  # bytes -> str 자동 변환
)
