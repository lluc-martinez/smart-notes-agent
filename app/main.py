from fastapi import FastAPI, Header, HTTPException
import logging

# Import your configuration (where .env is loaded)
from app.core.config import settings

# Import your schemas and business logic.
# (Adjust these two lines if your file or folder names are different.)
from app.schemas.telegram_schemas import TelegramUpdate
from app.services.message_handler import process_telegram_update

# Basic logging configuration for viewing errors in TrueNAS
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Smart Notes Agent")

@app.get("/")
async def root():
    """Health endpoint for quickly checking whether the container is running."""
    return {"status": "ok", "message": "Smart Notes Agent is running!"}

@app.post("/webhook")
async def telegram_webhook(
    update: TelegramUpdate,
    x_telegram_bot_api_secret_token: str = Header(None)
):
    """Official endpoint that receives Telegram messages."""
    
    # 1. Verify that the request comes from Telegram by comparing the secret token
    if x_telegram_bot_api_secret_token != settings.TELEGRAM_SECRET_TOKEN:
        logger.warning("Blocked an unauthorized webhook access attempt.")
        raise HTTPException(status_code=403, detail="Forbidden: Invalid secret token")
    
    # 2. Process the message asynchronously
    try:
        await process_telegram_update(update)
    except Exception as e:
        logger.error(f"Internal error processing the message: {e}")
        # Return 200 OK even if there is an error in our logic.
        # If we return a 500 error to Telegram, it will repeatedly resend the same message.
        return {"status": "error", "detail": str(e)}

    # 3. Confirm to Telegram that the message was received successfully
    return {"status": "ok"}