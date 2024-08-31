import asyncio

from src.auth.utils import decode_access
from fastapi import WebSocket



class WSConnectionManager:
    def __init__(self, access_token: str) -> None:
        self.active_connections: list[WebSocket] = []
        self.access_token = access_token
        self.user_id = 0

    async def connect(self, websocket: WebSocket) -> None:
        user_id = await decode_access(self.access_token)
        if not user_id:
            self.active_connections.remove(websocket)
        self.user_id = int(user_id)
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def send_json_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_json(message)
        await asyncio.sleep(2)