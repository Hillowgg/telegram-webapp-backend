import json
from pprint import pprint
import uuid

from tortoise import Tortoise, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
# from tortoise.contrib.fastapi import register_tortoise
import db_models


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": [db_models]})
    await Tortoise.generate_schemas()

    calendar = await db_models.Calendar.create(uuid=uuid.uuid4())
    user = await db_models.CalendarUser.create(calendar=calendar, telegram_id=1, permission='owner')
    user1 = await db_models.CalendarUser.create(calendar=calendar, telegram_id=2, permission='editor')
    timetable = await db_models.TimeTable.create(calendar=calendar, name='test')

    task = await db_models.Task.create(timetable=timetable, day_of_week='monday', week_parity=False,
                                       name='test',
                                       start_time=123, end_time=456)

    # print(await db_models.Calendar.all())
    calendar_pydan = pydantic_model_creator(db_models.Calendar, name="Calendar")

    pprint(json.loads((await calendar_pydan.from_tortoise_orm(calendar)).json()))


if __name__ == "__main__":
    run_async(run())
