from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from strawberry.asgi import GraphQL
from message import get_chat_history, log_message_to_db, get_user_by_id, get_user_by_email, fetch_friend_list, log_user
from connection_manager import ConnectionManager
from fastapi.middleware.cors import CORSMiddleware
from middleware import LoggingMiddleware
from mygraphql.schema import schema


AUTH_SERVICE_URL = "https:///ui-app-745799261495.us-east4.run.app"

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

graphql_app = GraphQL(schema)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

@app.get("/")
async def read_root():
    return {"message": "Here is Chat Service API"}

@app.get("/chat-history/{sender_id}/{recipient_id}")
async def chat_history(sender_id: int, recipient_id: int):
    history = get_chat_history(sender_id, recipient_id)
    return {"history": history}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    try:
        user_info = get_user_by_id(user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found")
        username = user_info["username"]
        
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

@app.get("/get-user-id/{user_id}")
async def get_user_id(user_id: int):
    user = get_user_by_id(user_id)
    if user:
        return {"user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@app.get("/get-user-email")
async def get_user_email(email: str):
    user = get_user_by_email(email)
    if user:
        return {"user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/friend-list/{user_id}")
async def get_friend_list(user_id: int):
    friends = fetch_friend_list(user_id)
    return {"friends": friends}


@app.post("/auth/google-login")
async def google_login(request: Request):

    try:
        data = await request.json()
        email = data.get("email")
        username = data.get("username")

        if not email or not username:
            raise HTTPException(status_code=400, detail="Missing email or username")

        log_user(email, username)
        return {"message": "User logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log user: {str(e)}")
