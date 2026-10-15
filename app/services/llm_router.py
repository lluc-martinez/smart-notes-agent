import json
from datetime import datetime
from openai import AsyncOpenAI
from app.core.config import settings
from app.schemas.llm_schemas import RouterOutput

client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=settings.NVIDIA_API_KEY
)

async def analyze_intent(text: str) -> RouterOutput:
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    day_of_week = now.strftime("%A")

    system_prompt = f"""
    You are the intelligent router for a personal assistant bot.
    Your only job is to analyze the user's message, deduce their intent, and extract key data.
    
    Current Date: {current_date} ({day_of_week})
    Current Time: {current_time}
    
    You MUST respond with a valid JSON object matching this schema:
    {{
        "intent": "shopping" | "calendar" | "note",
        "action": "add" | "remove" | "read",
        "entities": {{ ... }},
        "reply_summary": "Short confirmation message in the language of the user."
    }}
    
    Rules for 'entities':
    - shopping: return {{"items": ["item1", "item2"]}}.
    - calendar: return {{"title": "event name", "date": "YYYY-MM-DD", "time": "HH:MM", "duration_minutes": 60}}.
    - note: return {{"tags": ["tag1"], "content": "full text of the idea/link"}}.
    
    If ambiguous, default to "note".
    """

    response = await client.chat.completions.create(
        model="openai/gpt-oss-20b", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.0
    )

    raw_json = response.choices[0].message.content
    
    if raw_json.startswith("```json"):
        raw_json = raw_json.strip("```json").strip("```").strip()

    parsed_dict = json.loads(raw_json)
    return RouterOutput(**parsed_dict)

async def generate_natural_response(user_input: str, db_context: str) -> str:
    """
    Takes the raw data from the database and uses the LLM to formulate 
    a natural, friendly response answering the user's query.
    """
    system_prompt = f"""
    You are a helpful personal assistant. The user has asked a question about their saved data.
    
    Here is the raw data retrieved from their database:
    ---
    {db_context}
    ---
    
    Your task:
    1. Answer the user's question using ONLY the provided data.
    2. Write in a natural, conversational and friendly tone.
    3. Respond in the same language the user used.
    4. Do not mention "the database", "JSON", or "the provided data". Just act like you remember it.
    """

    response = await client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3  # Slightly higher for more natural language generation
    )
    
    return response.choices[0].message.content