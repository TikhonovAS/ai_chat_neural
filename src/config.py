import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Централизованные настройки проекта. Аналог 'менеджера сейфа'."""
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "true").lower() == "true"
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "mock")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "llama3.2:3b")

    # Пути к файлам
    HISTORY_FILE: str = os.getenv("HISTORY_FILE", "history.json")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/bot.log")