import os
import hmac, hashlib
from collections import OrderedDict

from fastapi import FastAPI, Header, Query, Depends

from telegram_models import *

TELEGRAM_BOT_TOKEN = os.getenv("TOKEN")





async def validate_request(telegram_data: WebAppInitData):
    data_check_string = '\n'.join([f'{k}={v}' for k, v in OrderedDict(telegram_data.dict()) if k != 'hash'])

    secret = hmac.new(msg=TELEGRAM_BOT_TOKEN.encode('utf-8'), key=b'WebAppData', digestmod=hashlib.sha256)

    true_hash = hmac.new(msg=data_check_string.encode('utf-8'), key=secret.digest(),
                         digestmod=hashlib.sha256).hexdigest()

    return true_hash == telegram_data.hash


app = FastAPI()


@app.get("/api/calendar", tags=["calendar"], dependencies=[Depends(validate_request)])
async def get_calendar(
        calendar_uuid: str = Query(..., alias="id"),
        telegram_data: WebAppInitData | None = Header(...),
        depends: Depends = Depends(validate_request)):
    return
