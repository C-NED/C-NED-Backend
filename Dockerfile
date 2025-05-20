# 베이스 이미지
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치 (예: gcc, mysqlclient 쓰면 필요)
# RUN apt-get update && apt-get install -y build-essential default-mysql-client

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 앱 코드 복사
COPY . .

# 앱 실행 (fly는 8080 포트 기준이므로 꼭 맞춰야 함)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
