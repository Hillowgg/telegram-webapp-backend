import hashlib
import hmac
import os

from fastapi import FastAPI, Query, HTTPException, Depends, Body
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.src.body_models import APICalendarData, APITaskData
from backend.src.db_models import Calendar, CalendarUser
from backend.src.telegram_models import WebAppInitData

TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")
app = FastAPI()


async def validate_request(telegram_data: WebAppInitData):
    # print(telegram_data.json(exclude_none=True))
    data_check_string = "\n".join(
        sorted([f'{k}={v}' for k, v in telegram_data.dict(exclude_none=True).items() if k != 'hash']))

    data_check_string = data_check_string.replace("'", '"').replace(' ', '')

    secret = hmac.new(msg=TELEGRAM_BOT_TOKEN.encode('utf-8'), key=b'WebAppData', digestmod=hashlib.sha256)

    true_hash = hmac.new(msg=data_check_string.encode('utf-8'), key=secret.digest(),
                         digestmod=hashlib.sha256).hexdigest()
    return true_hash == telegram_data.hash


@app.post("/api/calendar", tags=["calendar"],
          dependencies=[Depends(validate_request)]
          )
# @validate_request
async def get_calendar(
        calendar_uuid: str = Query(..., alias="calendar_uuid"),
        telegram_data: APICalendarData | None = Body(...),
        allowed: Depends = Depends(validate_request)
):
    if not allowed:
        raise HTTPException(status_code=403, detail='Wrong credentials')

    Calendar_pydantic = pydantic_model_creator(Calendar, name="Calendar")

    calendar_fetch = await Calendar.filter(uuid=calendar_uuid).first()
    calendar_pydantic = await Calendar_pydantic.from_tortoise_orm(calendar_fetch)

    if not calendar_fetch:
        return HTTPException(status_code=404, detail="Calendar not found")

    user = await CalendarUser.filter(calendar=calendar_fetch, telegram_id=197196058).first()

    if user is None:
        raise HTTPException(status_code=403, detail="Permission denied")

    return calendar_pydantic.timetables


@app.post('/api/calendar/create')
async def create_calendar():
    return NotImplemented


@app.post('/api/calendar/add_user')
async def add_user_to_calendar():
    return NotImplemented


@app.post('/api/calendar/remove_user')
async def remove_user_from_calendar():
    return NotImplemented


@app.post('/api/calendar/change_user_role')
async def change_user_role():
    return NotImplemented


@app.post("/api/task/add")
async def add_task(
        calendar_uuid: str = Query(..., alias="calendar_uuid"),
        data: APITaskData = Body(...),
        allowed: Depends = Depends(validate_request)
):
    if not allowed:
        raise HTTPException(status_code=403, detail='Wrong credentials')

    Calendar_pydantic = pydantic_model_creator(Calendar, name="Calendar")

    calendar_fetch = await Calendar.filter(uuid=calendar_uuid).first()
    calendar_pydantic = await Calendar_pydantic.from_tortoise_orm(calendar_fetch)

    if not calendar_fetch:
        return HTTPException(status_code=404, detail="Calendar not found")

    user = await CalendarUser.filter(calendar=calendar_fetch, telegram_id=197196058).first()

    if user is None or user.permission < 1:
        raise HTTPException(status_code=403, detail="Permission denied")

    return NotImplemented


@app.post('/api/task/remove_by_id')
async def remove_task():
    return NotImplemented


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["backend.src.db_models"]},
    generate_schemas=False,
    add_exception_handlers=True
)

# "query_id=AAEa-cALAAAAABr5wAsl8McX&user={"id":197196058,"first_name":"Hillow","last_name":"","username":"Hillow","language_code":"en"}&auth_date=1676290535&hash=05a2fad9bae858663aacdba807dc986588b0ccbafb3f221baa48d493ecf0ed2e"
