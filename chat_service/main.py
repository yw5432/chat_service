from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from models import User, GroupCreate, JoinRequest
from user import register_user, authenticate_user
from message import get_chat_history, log_message_to_db
from group import create_group, join_group
from connection_manager import ConnectionManager

app = FastAPI()

manager = ConnectionManager()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Chat Service API!"}

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

@app.post("/create-group")
async def create_group_endpoint(group: GroupCreate):
    return create_group(group, manager)

@app.post("/join-group")
async def join_group_endpoint(request: JoinRequest):
    return join_group(request, manager)

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
            if data.startswith("group:"):
                _, group_name, message = data.split(":", 2)
                log_message_to_db(sender=username, group_name=group_name, message=message)
                await manager.send_group_message(group_name, f"{username}: {message}")
            else:
                recipient, message = data.split(":", 1)
                log_message_to_db(sender=username, recipient=recipient, message=message)
                await manager.send_private_message(f"{username}: {message}", recipient)
    except WebSocketDisconnect:
        manager.disconnect(websocket)