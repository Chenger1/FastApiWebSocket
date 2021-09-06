from fastapi import APIRouter, WebSocket, FastAPI


ws = FastAPI()


@ws.websocket_route('/echo_handler')
async def echo_handler(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f'Message: {data}')
