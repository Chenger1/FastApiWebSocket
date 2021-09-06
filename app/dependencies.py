from fastapi import WebSocket, WebSocketDisconnect

from typing import Optional


async def get_user(websocket: WebSocket) -> Optional[str]:
    username = websocket.query_params.get('username')
    if not username:
        raise WebSocketDisconnect(code=1002)
    return username
