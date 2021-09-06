from fastapi import WebSocket, FastAPI, WebSocketDisconnect

from connection_manager import manager


ws = FastAPI()


@ws.websocket_route('/echo_handler')
async def echo_handler(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f'Message: {data}')


@ws.websocket('/{username}')
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f'You wrote: {data}', websocket)
            await manager.broadcast(f'New message: {data}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f'Client {username} left chat')
