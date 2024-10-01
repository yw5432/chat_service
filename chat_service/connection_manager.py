from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections = {}
        self.group_members = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[username] = websocket

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        user_to_remove = None
        for user, ws in self.user_connections.items():
            if ws == websocket:
                user_to_remove = user
                break
        if user_to_remove:
            del self.user_connections[user_to_remove]
            for group_name, members in self.group_members.items():
                if user_to_remove in members:
                    members.remove(user_to_remove)

    async def send_private_message(self, message: str, recipient: str):
        recipient_socket = self.user_connections.get(recipient)
        if recipient_socket:
            await recipient_socket.send_text(message)

    def add_user_to_group(self, username: str, group_name: str):
        if group_name not in self.group_members:
            self.group_members[group_name] = set()
        self.group_members[group_name].add(username)

    async def send_group_message(self, group_name: str, message: str):
        if group_name in self.group_members:
            members = self.group_members[group_name]
            for member in members:
                member_socket = self.user_connections.get(member)
                if member_socket:
                    await member_socket.send_text(message)
