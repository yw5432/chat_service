from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from message import get_chat_history, log_message_to_db, get_user_by_id
from connection_manager import ConnectionManager
from fastapi.middleware.cors import CORSMiddleware
from middleware import LoggingMiddleware

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
    return {"message": "It is Chat Service API"}

@app.get("/chat-history")
async def chat_history(sender: str, recipient: str):
    history = get_chat_history(sender, recipient)
    return {"history": history}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            recipient, message = data.split(":", 1)
            log_message_to_db(sender=username, recipient=recipient, message=message)
            await manager.send_private_message(f"{username}: {message}", recipient)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/get-user-id")
async def get_user_id(userid: int):
    user = get_user_by_id(userid)
    if user:
        return {"user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found")