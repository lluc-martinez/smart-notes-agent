from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Depends
from app.schemas.telegram_schemas import TelegramUpdate
from app.services.message_handler import process_telegram_update
from app.core.config import settings

router = APIRouter()

# Optional: Add a secret token in the URL to prevent random internet scans from hitting your webhook
WEBHOOK_PATH = f"/webhook/{settings.TELEGRAM_BOT_TOKEN}"

@router.post(WEBHOOK_PATH)
async def telegram_webhook(
    update: TelegramUpdate,
    background_tasks: BackgroundTasks
):
    """
    Endpoint that receives updates from Telegram.
    Returns 200 OK immediately and processes the message in the background.
    """
    # 1. Add the actual processing logic to background tasks
    background_tasks.add_task(process_telegram_update, update)
    
    # 2. Return immediately to satisfy Telegram's timeout requirements
    return {"status": "ok"}