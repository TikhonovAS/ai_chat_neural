import logging
from src.config import Settings

logger = logging.getLogger(__name__)


class AIClient:
    """Клиент для взаимодействия с ИИ. Поддерживает режим отладки (mock)."""

    def __init__(self, provider: str = Settings.AI_PROVIDER):
        self.provider = provider

    def get_response(self, messages: list[dict]) -> str:
        """Возвращает ответ от ИИ или mock-заглушку в режиме отладки."""
        if Settings.DEBUG_MODE:
            logger.debug("🧪 DEBUG_MODE активен: используется mock-ответ")
            last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "нет сообщения")
            return f" [MOCK-контекст]\nВижу {len(messages)} сообщений.\nПоследнее от тебя: {last_user_msg[:30]}..."

        # Здесь будет реальная интеграция (Ollama/HF/Groq)
        # Для тестов достаточно mock-ветки выше
        return "🤖 Реальный ответ от ИИ (интеграция в разработке)"