from fastapi import WebSocket, FastAPI, WebSocketDisconnect

from connection_manager import manager, layer_manager


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


@ws.websocket('/chat/{chat_id}')
async def websocket_chat(websocket: WebSocket, chat_id: int):
    conn_manager = await layer_manager.connect_to_manager(chat_id)
    await conn_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await conn_manager.send_personal_message(f'You wrote: {data}', websocket)
            await conn_manager.broadcast(f'New message: {data}')
    except WebSocketDisconnect:
        conn_manager.disconnect(websocket)
        await conn_manager.broadcast(f'Client left chat')
