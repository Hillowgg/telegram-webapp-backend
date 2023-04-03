import hashlib
import hmac
from typing import Annotated

from fastapi import HTTPException, Depends, status

from backend.src.CONSTANTS import TELEGRAM_BOT_TOKEN
from backend.src.models.models import Calendar
from backend.src.telegram_models import WebAppInitData


async def telegram_credentials_validation(telegram_credentials: WebAppInitData,
                                          telegram_token=Depends(TELEGRAM_BOT_TOKEN)):
    data_check_string = '\n'.join(
        sorted([f'{k}={v}' for k, v in telegram_credentials.dict(exclude_none=True).items() if k != 'hash']))

    data_check_string = data_check_string.replace('\'', '\"').replace(' ', '')

    secret = hmac.new(msg=telegram_token.encode('utf-8'), key=b'WebAppData', digestmod=hashlib.sha256)

    true_hash = hmac.new(msg=data_check_string.encode('utf-8'), key=secret.digest(),
                         digestmod=hashlib.sha256).hexdigest()
    if true_hash != telegram_credentials.hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong telegram credentials",
        )
    return telegram_credentials


async def get_calendar(uuid: str):
    calendar = await Calendar.filter(uuid=uuid).first()
    if not calendar:
        return HTTPException(status_code=404, detail='Calendar not found')

    return calendar


TelegramDep = Annotated[WebAppInitData, Depends(telegram_credentials_validation)]
CalendarDep = Annotated[str, Depends(get_calendar)]
