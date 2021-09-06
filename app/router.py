from fastapi import APIRouter, HTTPException

from redis_db import redis_manager


router = APIRouter(
    prefix='/auth'
)


@router.post('/sign-up')
async def sign_up(username: str):
    users = await redis_manager.manual_get('hgetall', 'users')
    last_id = await redis_manager.manual_get('get', 'user_id')
    if username in users.keys():
        raise HTTPException(
            detail='User with this username already exists',
            status_code=404
        )
    new_id = int(last_id) + 1
    users[new_id] = username

    await redis_manager.manual_set('hmset', 'users', users)
    await redis_manager.manual_set('set', 'user_id', new_id)
    return {
        'username': username,
        'user_id': new_id,
        'status': 200
    }


@router.get('/users')
async def users_list():
    users = await redis_manager.manual_get('hgetall', 'users')
    return {'users': users}
