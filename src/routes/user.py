from fastapi import APIRouter

from backend.src.dependencies.dependencies import TelegramDep

router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses={404: {'description': 'Not found'}}
)

@router.post('/calendar/{uuid}/user/add')
async def add_user_to_calendar(telegram_credentials: TelegramDep, uuid: str):
    return NotImplemented


@router.post('/calendar/{uuid}/user/remove')
async def remove_user_from_calendar(telegram_credentials: TelegramDep, uuid: str):
    return NotImplemented


@router.post('/calendar/{uuid}/user/change_role')
async def change_user_role(telegram_credentials: TelegramDep, uuid: str):
    return NotImplemented
