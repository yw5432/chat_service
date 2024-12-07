from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from message import get_chat_history, log_message_to_db, get_user_by_id
from connection_manager import ConnectionManager
from fastapi.middleware.cors import CORSMiddleware
from middleware import LoggingMiddleware
import httpx

AUTH_SERVICE_URL = "https://user-auth-service-745799261495.us-east4.run.app"

app = FastAPI()

manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Here is Chat Service API"}

@app.get("/chat-history")
async def chat_history(sender_id: int, recipient_id: int):
    history = get_chat_history(sender_id, recipient_id)
    return {"history": history}

@app.websocket("/ws/{id}/{username}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        await manager.connect(websocket, user_id)
    except Exception as e:
        await websocket.close()
        raise HTTPException(status_code=401, detail="Failed to connect WebSocket")

    try:
        while True:
            data = await websocket.receive_text()
            recipient_id, message = data.split(":", 1)

            try:
                recipient_id = int(recipient_id)
                log_message_to_db(sender_id=user_id, recipient_id=recipient_id, message=message)
                await manager.send_private_message(f"{username}: {message}", recipient_id)
            except Exception as e:
                await websocket.send_text(f"Error processing message: {str(e)}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/get-user-id")
async def get_user_id(userid: int):
    user = get_user_by_id(userid)
    if user:
        return {"user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found")