from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter()

@router.websocket("/ws/ai")
async def ai_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            print("🧠 AI Data:", data)
            # DB 저장 또는 프론트로 브로드캐스트
    except WebSocketDisconnect:
        print("❌ AI 연결 종료")
