from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Notes Agent"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_SECRET_TOKEN: str
    ALLOWED_USER_ID: int
    
    # OpenAI / LLM
    OPENAI_API_KEY: str
    NVIDIA_API_KEY: str
    GROQ_API_KEY: str
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/smart_notes.db"
    
    # Security
    SECRET_KEY: str  # For signing cookies or JWTs if needed in the OAuth flow

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Global instance to import throughout the app
settings = Settings()