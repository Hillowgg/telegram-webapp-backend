from fastapi import APIRouter, HTTPException

from backend.src.dependencies.dependencies import TelegramDep
from backend.src.models.models import Calendar, CalendarUser, Task, Task_pydantic

router = APIRouter(
    prefix='/task',
    tags=['task'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/calendar/{uuid}/task/add')
async def add_task(
        uuid: str,
        telegram_credentials: TelegramDep,
        task: Task_pydantic
):
    calendar_fetch = await Calendar.filter(uuid=uuid).first()

    if not calendar_fetch:
        return HTTPException(status_code=404, detail='Calendar not found')

    user = await CalendarUser.filter(calendar=calendar_fetch, telegram_id=telegram_credentials.user.id).first()

    if user is None or user.permission < 1:
        raise HTTPException(status_code=403, detail='Permission denied')

    res = await Task.create(task)

    if res is None:
        raise HTTPException(status_code=500, detail='Failed to add task')


@router.post('/calendar/{uuid}/task/remove_by_id')
async def remove_task(
        uuid: str,
        telegram_credentials: TelegramDep,

):
    return NotImplemented
