(2025.4.1 기준)

# 🚀 C-NED Backend

🔥 배포된 서비스 링크: 👉 [C-NED API 문서](https://port-0-c-ned-backend-m8d025yhc9939d4f.sel4.cloudtype.app/docs)  
📑 전체 개발 문서: 👉 [Notion 바로가기](https://www.notion.so/1afbb4312b768015945ee3bf76a6a7d3)

---

## 🧱 데이터베이스 구조

앱 **Doby** 및 관리자 웹 **Dorocy**에서 사용되는 **통합 DB 구조 설계가 완료**되었습니다.  
주요 기능에 따라 테이블이 구분되며, 실시간 주행 정보 및 AI 감지 데이터를 효율적으로 처리할 수 있도록 설계되었습니다.

- 📍 주요 테이블:
  - `navigation`, `path`, `road_section` – 경로 및 주행 정보
  - `outbreak`, `caution`, `dangerous_incident`, `vsl` – 교통 돌발 상황 및 위험 정보
  - `user`, `admin`, `refresh_token` – 사용자 및 인증 관리

> 이 설계는 실시간 데이터 스트리밍(WebSocket)과 이벤트 기반 데이터 저장 구조를 모두 고려하여 구축되었습니다.

---

### 🔹 시스템 추상 구조 (Crow’s Foot 모델)

> 각 주요 엔터티 간의 관계를 **Crow’s Foot 다이어그램**으로 표현한 추상 설계입니다.

<img src="docs/images/cned_crows_foot.jpg" width="550"/>

---

### 🔸 상세 테이블 설계 (URL 클래스 다이어그램)

> 실제 구현에 사용된 **정규화된 테이블 구조와 필드 정의**를 포함한 상세 설계입니다.

<img src="docs/images/cned_url_class_diagram.jpg" width="620"/>


> 📘 **자세한 필드 설명과 제약 조건은 [Notion 문서](https://pouncing-toothpaste-a07.notion.site/DB-1babb4312b7680368fe4f63a87575891?pvs=4)를 참고해주세요.**

---

## 📌 프로젝트 구성

### 🛣️ 앱 (Doby)
- AI 기반 실시간 네비게이션
- 도로 위험 요소 감지 및 안내

### 🖥️ 관리자 웹 (Dorocy)
- 감지 정보 시각화
- AI 성능 모니터링 대시보드

---

## 🔧 기술 스택

- **Backend**: FastAPI  
- **DB**: MariaDB + Redis  
- **외부 API**: 네이버 개발자센터 오픈 API, 네이버 클라우드 플랫폼 MAPS API, ITS 공공 API
- **배포**: cloudtype

---

## 🚧 진행 상황

| 항목 | 상태 |
|------|------|
| 📦 DB 설계 및 구축 | ✅ 완료 (앱/웹 통합) |
| 🔐 인증 시스템 | 🛠 구현 중 (JWT + Redis + Refresh Token) |
| 📡 실시간 API | 🔜 WebSocket 구조 설계 예정 |
| 🚀 배포 브랜치 | `main` 유지 / `test`에서 개발 중 |

> 📋 상세 개발 기록 및 작업 흐름은 Notion에서 확인하세요 → [🔗 Notion 바로가기](https://www.notion.so/1afbb4312b768015945ee3bf76a6a7d3)
<br>작업 상황은 주기적으로 업데이트 될 예정입니다
