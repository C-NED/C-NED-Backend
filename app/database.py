from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.key_collection import SQLALCHEMY_DATABASE_URL

Base = declarative_base()

# DB 연결
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"charset": "utf8mb4"})

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()