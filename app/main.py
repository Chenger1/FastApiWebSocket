from fastapi import FastAPI
import uvicorn

from redis_db import redis_manager


app = FastAPI()


@app.on_event('startup')
async def startup_event():
    await redis_manager.init_redis()


@app.on_event('shutdown')
async def shutdown_event():
    await redis_manager.close()


if __name__ == '__main__':
    uvicorn.run(app)
