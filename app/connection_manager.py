from fastapi import WebSocket


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

    async def broadcast(self, message: str):
        for connection in self.active_connection:
            await connection.send_text(message)


manager = ConnectionManager()


class ConnectionLayerManager:
    def __init__(self):
        self.active_manager: dict[int, ConnectionManager] = {}

    async def connect_to_manager(self, layer_id: int):
        conn_manager = self.active_manager.setdefault(layer_id, ConnectionManager())
        return conn_manager


layer_manager = ConnectionLayerManager()
