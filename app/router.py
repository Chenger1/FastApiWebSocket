from fastapi import APIRouter


router = APIRouter(
    prefix='auth/'
)


@router.post('/sign-up')
async def sign_up(username: str, password: str):
    pass
