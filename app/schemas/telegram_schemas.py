from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class TelegramUser(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: Optional[str] = None

class TelegramChat(BaseModel):
    id: int
    type: str

class TelegramVoice(BaseModel):
    file_id: str
    duration: int
    mime_type: Optional[str] = None

class TelegramMessage(BaseModel):
    message_id: int
    from_user: Optional[TelegramUser] = Field(None, alias="from")
    chat: TelegramChat
    date: int
    text: Optional[str] = None
    voice: Optional[TelegramVoice] = None

class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] = None
    
    # Allow extra fields since Telegram sends a lot of data we don't need
    model_config = {"extra": "ignore"}