import logging
from app.schemas.telegram_schemas import TelegramUpdate
from app.services.llm_router import analyze_intent, generate_natural_response
from app.services.telegram_client import send_telegram_message
from app.services.db_service import execute_action, get_shopping_list, get_notes_context
from app.services.audio_service import transcribe_audio

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_user_text(user_text: str, chat_id: int, user_name: str) -> None:
    """Core function: Process text regardless of whether it comes from typing or voice."""
    if user_text.startswith("/llista"):
        llista_text = get_shopping_list(chat_id)
        await send_telegram_message(chat_id, llista_text)
        return

    logger.info(f"Processing text from {user_name}: {user_text}")
    
    try:
        router_result = await analyze_intent(user_text)
        logger.info(f"LLM parsed result: {router_result.model_dump_json()}")
        
        if router_result.action == "read":
            if router_result.intent == "shopping":
                db_context = get_shopping_list(chat_id)
            elif router_result.intent == "note":
                db_context = get_notes_context(chat_id)
            else:
                db_context = "No data available."

            bot_reply = await generate_natural_response(user_text, db_context)
            await send_telegram_message(chat_id, bot_reply)
            
        else:
            await send_telegram_message(chat_id, router_result.reply_summary)
            execute_action(router_result, chat_id, user_name)
            
    except Exception as e:
        logger.error(f"Error in LLM/DB processing: {e}")
        await send_telegram_message(chat_id, "⚠️ There was an error processing your request.")

async def process_telegram_update(update: TelegramUpdate) -> None:
    """Webhook entry point."""
    if not update.message:
        return

    chat_id = update.message.chat.id

    if chat_id != settings.ALLOWED_USER_ID:
        print(f"Unauthorized access attempt from chat_id: {chat_id}")
        await send_telegram_message(chat_id, "⚠️ You are not authorized to use this bot.")
        return

    user_name = update.message.from_user.first_name if update.message.from_user else "Unknown"

    if update.message.text:
        await handle_user_text(update.message.text, chat_id, user_name)
            
    elif update.message.voice:
        logger.info(f"Received voice message from {user_name}")
        await send_telegram_message(chat_id, "⏳ Listening to your audio...")
        
        try:
            # 1. Transcribe the audio
            transcribed_text = await transcribe_audio(update.message.voice.file_id)
            logger.info(f"Transcribed text: {transcribed_text}")
            
            # 2. Pass it to the brain in the same way as text
            await handle_user_text(transcribed_text, chat_id, user_name)
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            await send_telegram_message(chat_id, "⚠️ I couldn't transcribe the audio.")