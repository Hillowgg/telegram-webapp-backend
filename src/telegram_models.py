from pydantic import BaseModel

class WebAppChat(BaseModel):
    id: int
    type: str
    title: str
    username: str | None
    photo_url: str | None


class WebAppUser(BaseModel):
    id: int
    is_bot: bool | None
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    is_premium: bool | None
    photo_url: str | None


class WebAppInitData(BaseModel):
    query_id: str | None
    user: WebAppUser | None
    receiver: WebAppUser | None
    chat: WebAppChat | None
    start_param: str | None
    can_send_after: int | None
    auth_date: int | None
    hash: str | None