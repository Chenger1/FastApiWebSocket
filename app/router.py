from fastapi import APIRouter, HTTPException

from redis_db import redis_manager


router = APIRouter(
    prefix='/auth'
)


@router.post('/sign-up')
async def sign_up(username: str, password: str):
    users = await redis_manager.get('users') or {}
    if username in users.keys():
        raise HTTPException(
            detail='User with this username already exists',
            status_code=404
        )
    users[username] = password  # Save plain password only for learning purposes.
    await redis_manager.manual_set('hmset', 'users', users)
    return {
        'username': username,
        'password': password,
        'status': 200
    }


@router.get('/users')
async def users_list():
    users = await redis_manager.manual_get('hgetall', 'users')
    return {'users': users}
