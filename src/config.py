import os
from dotenv import load_dotenv

# Загружаем переменные из .env в окружение Python
# Если .env нет (например, в CI/CD), load_dotenv просто проигнорирует шаг
load_dotenv()


class Settings:
    """
    Класс-хранилище настроек проекта.
    Аналогия: "менеджер сейфа" — он знает, где лежат ключи и модели,
    но не раскрывает их напрямую в логике бота.
    """

    # Берём ключ из окружения. Если его нет — вызываем ошибку сразу,
    # а не ловим её посередине работы бота.
    # Провайдер: 'hf' (Hugging Face) / 'openrouter' / 'mock'
    AI_PROVIDER = os.getenv("AI_PROVIDER", "hf")

    # Ключи
    HF_API_KEY = os.getenv("HF_API_KEY", "")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

    # URL API (Hugging Face поддерживает OpenAI-формат)
    HF_API_URL = "https://api-inference.huggingface.co/v1/chat/completions"
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

    # Модель по умолчанию
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "Qwen/Qwen2.5-7B-Instruct")

    # Режим отладки
    DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"

    # Валидация при старте
    if not DEBUG_MODE and AI_PROVIDER == "hf" and not HF_API_KEY:
        raise ValueError("HF_API_KEY не найден в .env! Получи на huggingface.co/setting/tokens")
