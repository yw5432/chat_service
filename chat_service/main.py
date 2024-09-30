from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from models import User
from user import register_user, authenticate_user
from message import get_chat_history, log_message_to_db
from connection_manager import ConnectionManager

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "hello!"}

@app.post("/register")
async def register(user: User):
    result = register_user(user.username, user.password)
    if result["status"] == "success":
        return result
    else:
        raise HTTPException(status_code=500, detail=result["message"])

@app.post("/login")
async def login(user: User):
    if authenticate_user(user.username, user.password):
        return {"status": "success", "message": "Logged in successfully."}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/chat-history")
async def chat_history(sender: str, recipient: str):
    history = get_chat_history(sender, recipient)
    return {"history": history}

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = data.split(":", 1)
            if len(message_data) == 2:
                recipient, message = message_data
                log_message_to_db(sender=username, recipient=recipient, message=message)
                await manager.send_private_message(f"{username}: {message}", recipient)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

