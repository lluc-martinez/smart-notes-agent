# 🧠 Smart Notes Agent

An intelligent, AI-powered Telegram bot that acts as a "second brain" to organize messy messages, voice notes, and ideas into structured data.

Instead of having a chaotic "Saved Messages" chat, this agent listens to your text and audio, deduces your intent using Large Language Models, and automatically categorizes the information into actionable items (like shopping lists or tagged notes).

## ✨ Features

- **🎙️ Multimodal Input:** Seamlessly process both standard text messages and voice notes.
- **⚡ Fast Audio Transcription:** Integrates **Groq API** (`whisper-large-v3`) to transcribe Telegram voice messages in milliseconds.
- **🧠 Smart Intent Routing:** Uses **NVIDIA API** (`gpt-oss-20b`) to parse natural language and strictly classify the user's intent into a structured JSON schema.
- **🛒 Smart Shopping List:** Automatically add or cross off items from your grocery list.
- **📝 Tagged Notes:** Save links, ideas, or reminders with auto-generated contextual tags.
- **💬 Natural Conversation:** Uses your saved database context to reply organically to queries using natural language generation.

## 🛠️ Tech Stack & Architecture

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) for high-performance webhook processing.
- **Database:** SQLite managed via **SQLModel** / SQLAlchemy.
- **AI Integrations:**
  - `openai/gpt-oss-20b` (via NVIDIA endpoints) for intent classification and natural responses.
  - `whisper-large-v3` (via Groq endpoints) for audio transcription.
- **Bot Interface:** Telegram Bot API (Webhook based).

## 🚀 Quickstart (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/lluc-martinez/smart_notes_agent.git
cd smart_notes_agent
```

### 2. Set up the Environment Variables

Create a .env file in the root directory and add your API keys:

```dotenv
PROJECT_NAME="Smart Notes Agent"
DATABASE_URL="sqlite:///./data/smart_notes.db"

# Telegram Credentials
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
TELEGRAM_SECRET_TOKEN="your_custom_secret_token"
ALLOWED_USER_ID=123456789  # Your personal Telegram ID for security

# AI Endpoints
NVIDIA_API_KEY="your_nvidia_api_key"
GROQ_API_KEY="your_groq_api_key"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

Note: To receive webhooks locally from Telegram, you will need to expose your local server using a tool like ngrok or Cloudflare Tunnels.

## 🔮 Future Roadmap

- [ ] **Google Calendar Integration:** Automatically detect dates/times and schedule events directly into Google Calendar (schema already prepared).