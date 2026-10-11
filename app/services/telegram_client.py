import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

async def send_telegram_message(chat_id: int, text: str) -> None:
    """
    Sends a text message back to the user via the Telegram Bot API.
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML" # Allows basic formatting like <b>bold</b> or <i>italic</i>
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"Failed to send message to Telegram: {e}")