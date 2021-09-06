from fastapi import WebSocket, WebSocketDisconnect

from typing import Optional


async def get_user(websocket: WebSocket) -> Optional[str]:
    username = websocket.query_params.get('username')
    if not username:
        await websocket.accept()  # Maybe there is better way to send user info about bad credentials
        await websocket.send_text('You did`nt provide credentials')
        await websocket.close()
        raise WebSocketDisconnect(code=1)
    return username
