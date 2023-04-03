from pydantic import BaseModel

from backend.src.telegram_models import WebAppInitData

class APIBodyABC(BaseModel):
    pass


class TaskData(BaseModel):
    name: str
    day_of_week: str
    week_parity: bool
    start_time: int
    end_time: int


class APICalendarData(APIBodyABC):
    pass


class APITaskData(APIBodyABC):
    task: TaskData
