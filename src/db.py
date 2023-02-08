import uuid

from tortoise import Tortoise, run_async
# from tortoise.contrib.fastapi import register_tortoise
import db_models

async def run():
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": [db_models]})
    await Tortoise.generate_schemas()

    calendar = await db_models.Calendar.create(uuid=uuid.uuid4())
    user = await db_models.CalendarUser.create(calendar=calendar, telegram_id=1, permission='owner')
    timetable = await db_models.TimeTable.create(calendar=calendar, name='test')
    day = await db_models.Day.create(timetable=timetable)

    print(await db_models.Calendar.all())


if __name__ == "__main__":
    run_async(run())