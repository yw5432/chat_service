from fastapi import WebSocket
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        user_to_remove = None
        for user_id, ws in self.user_connections.items():
            if ws == websocket:
                user_to_remove = user_id
                break
        if user_to_remove:
            del self.user_connections[user_to_remove]

    async def send_private_message(self, message: str, recipient_id: int):
        recipient_socket = self.user_connections.get(recipient_id)
        if recipient_socket:
            await recipient_socket.send_text(message)
