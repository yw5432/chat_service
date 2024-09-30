from fastapi import WebSocket
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[username] = websocket

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        for user, ws in self.user_connections.items():
            if ws == websocket:
                del self.user_connections[user]
                break

    async def send_private_message(self, message: str, recipient: str):
        recipient_socket = self.user_connections.get(recipient)
        if recipient_socket:
            await recipient_socket.send_text(message)