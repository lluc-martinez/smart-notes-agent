import os
import httpx
from openai import AsyncOpenAI
from app.core.config import settings

# Point the client to the Groq API
audio_client = AsyncOpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

async def get_telegram_file_path(file_id: str) -> str:
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()["result"]["file_path"]

async def download_audio(file_path: str, save_path: str) -> None:
    url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)

async def transcribe_audio(file_id: str) -> str:
    file_path = await get_telegram_file_path(file_id)
    
    local_filename = f"temp_{file_id}.ogg"
    await download_audio(file_path, local_filename)
    
    try:
        with open(local_filename, "rb") as audio_file:
            # Use Groq's free and extremely fast model
            transcription = await audio_client.audio.transcriptions.create(
                model="whisper-large-v3", 
                file=audio_file,
            )
        return transcription.text
    finally:
        if os.path.exists(local_filename):
            os.remove(local_filename)