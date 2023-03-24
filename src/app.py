import hashlib
import hmac
import os
from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, status
from tortoise.contrib.fastapi import register_tortoise

from backend.src.models import Calendar, CalendarUser, Calendar_pydantic, Task, Task_pydantic
from backend.src.telegram_models import WebAppInitData

TELEGRAM_BOT_TOKEN = os.getenv('TOKEN')
app = FastAPI()


async def telegram_credentials_validation(telegram_credentials: WebAppInitData):
    data_check_string = '\n'.join(
        sorted([f'{k}={v}' for k, v in telegram_credentials.dict(exclude_none=True).items() if k != 'hash']))

    data_check_string = data_check_string.replace('\'', '\"').replace(' ', '')

    secret = hmac.new(msg=TELEGRAM_BOT_TOKEN.encode('utf-8'), key=b'WebAppData', digestmod=hashlib.sha256)

    true_hash = hmac.new(msg=data_check_string.encode('utf-8'), key=secret.digest(),
                         digestmod=hashlib.sha256).hexdigest()
    if true_hash != telegram_credentials.hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong telegram credentials",
        )
    return telegram_credentials


TelegramDep = Annotated[WebAppInitData, Depends(telegram_credentials_validation)]


@app.post('/api/calendar')
async def get_calendar(telegram_credentials: TelegramDep):
    user_fetch = await CalendarUser.filter(telegram_id=telegram_credentials.user.id, permission=2).first()
    calendar_fetch = await Calendar.filter(users__id=user_fetch.id).first()

    calendar = await Calendar_pydantic.from_tortoise_orm(calendar_fetch)

    return calendar


@app.post('/api/calendar/{uuid}')
async def get_calendar_by_uuid(telegram_credentials: TelegramDep, uuid: str):
    calendar_fetch = await Calendar.filter(uuid=uuid).first()
    if not calendar_fetch:
        return HTTPException(status_code=404, detail='Calendar not found')

    user_fetch = await CalendarUser.filter(calendar=calendar_fetch, telegram_id=telegram_credentials.user.id).first()
    if user_fetch is None:
        raise HTTPException(status_code=403, detail='Permission denied')

    calendar = await Calendar_pydantic.from_tortoise_orm(calendar_fetch)

    return calendar.timetables


@app.post('/api/calendar/{uuid}/create')
async def create_calendar(telegram_credentials: TelegramDep, uuid: str):
    return NotImplemented


@app.post('/api/calendar/{uuid}/user/add')
async def add_user_to_calendar(telegram_credentials: TelegramDep, uuid: str):
    return NotImplemented


@app.post('/api/calendar/{uuid/user/remove')
async def remove_user_from_calendar(telegram_credentials: TelegramDep, uuid: str):
    return NotImplemented


@app.post('/api/calendar/{uuid}/user/change_role')
async def change_user_role(telegram_credentials: TelegramDep, uuid: str):
    return NotImplemented


@app.post('/api/calendar/{uuid}/task/add')
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


@app.post('/api/task/remove_by_id')
async def remove_task():
    return NotImplemented


@app.on_event("startup")
async def startup_event():
    register_tortoise(
        app,
        db_url='sqlite://db.sqlite3',
        modules={'models': ['backend.src.models']},
        generate_schemas=False,
        add_exception_handlers=True
    )

# 'query_id=AAEa-cALAAAAABr5wAsl8McX&user={'id':197196058,'first_name':'Hillow','last_name':'','username':'Hillow','language_code':'en'}&auth_date=1676290535&hash=05a2fad9bae858663aacdba807dc986588b0ccbafb3f221baa48d493ecf0ed2e'
