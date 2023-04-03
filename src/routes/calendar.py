from fastapi import APIRouter, HTTPException

from backend.src.dependencies.dependencies import TelegramDep, CalendarDep
from backend.src.models.models import Calendar, CalendarUser, Calendar_pydantic

router = APIRouter(
    prefix='/calendar',
    tags=['calendar'],
    responses={404: {'description': 'Not found'}}
)

@router.post('/calendar')
async def get_calendar(telegram_credentials: TelegramDep):
    user_fetch = await CalendarUser.filter(telegram_id=telegram_credentials.user.id, permission=2).first()
    calendar_fetch = await Calendar.filter(users__id=user_fetch.id).first()

    calendar = await Calendar_pydantic.from_tortoise_orm(calendar_fetch)

    return calendar


@router.post('/calendar/{uuid}')
async def get_calendar_by_uuid(
        telegram_credentials: TelegramDep,
        calendar_fetch: CalendarDep,
        uuid: str
):

    user_fetch = await CalendarUser.filter(calendar=calendar_fetch, telegram_id=telegram_credentials.user.id).first()
    if user_fetch is None:
        raise HTTPException(status_code=403, detail='Permission denied')

    calendar = await Calendar_pydantic.from_tortoise_orm(calendar_fetch)

    return calendar.timetables


@router.post('/calendar/create')
async def create_calendar(telegram_credentials: TelegramDep, uuid: str):
    return NotImplemented


