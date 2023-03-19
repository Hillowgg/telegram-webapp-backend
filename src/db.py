import json
from pprint import pprint
import uuid

from tortoise import Tortoise, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
# from tortoise.contrib.fastapi import register_tortoise
import db_models


async def init_db():
    await Tortoise.init(db_url="sqlite://data.sqlit3", modules={"models": [db_models]})
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()




async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": [db_models]})

    await Tortoise.generate_schemas()
    u1 = uuid.uuid4()
    u2 = uuid.uuid4()
    calendar1 = await db_models.Calendar.create(uuid=u1)
    await calendar1.save()
    calendar2 = await db_models.Calendar.create(uuid=u2)
    user = await db_models.CalendarUser.create(calendar=calendar1, telegram_id=1, permission='owner')
    await user.save()
    user1 = await db_models.CalendarUser.create(calendar=calendar2, telegram_id=2, permission='editor')
    await user1.save()
    timetable = await db_models.Timetable.create(calendar=calendar1, name='test')
    await timetable.save()

    task = await db_models.Task.create(timetable=timetable, day_of_week='monday', week_parity=False,
                                       name='test',
                                       start_time=123, end_time=456)
    await task.save()

    calendar = await db_models.Calendar.filter(uuid=u1).first()


    # await calendar.save()






if __name__ == "__main__":
    run_async(run())
