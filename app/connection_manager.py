from fastapi import WebSocket

from typing import Union


class ConnectionManager:
    def __init__(self):
        self.active_connection: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connection.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: Union[str, dict]):
        for connection in self.active_connection:
            if isinstance(message, str):
                await connection.send_text(message)
            elif isinstance(message, dict):
                await connection.send_json(message)


class ConnectionLayerManager:
    def __init__(self):
        self.active_manager: dict[int, ConnectionManager] = {}

    async def connect_to_manager(self, layer_id: int):
        conn_manager = self.active_manager.setdefault(layer_id, ConnectionManager())
        return conn_manager

    async def disconnect(self, websocket: WebSocket, layer_id: int):
        self.active_manager[layer_id].disconnect(websocket)
        if not self.active_manager[layer_id]:
            self.active_manager.pop(layer_id)

    async def cross_channel_broadcast(self, layer_id: int, data: Union[str, dict]):
        try:
            await self.active_manager[layer_id].broadcast(data)
        except KeyError:
            return


manager = ConnectionManager()
layer_manager = ConnectionLayerManager()
