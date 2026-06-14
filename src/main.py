import logging
from src.config import Settings
from src.logger import setup_logging
from src.chat_history import ChatHistory
from src.api_client import AIClient
from src.session import ChatSession


def main() -> None:
    """Точка входа: инициализация системы и запуск сессии."""
    setup_logging()  # ✅ Делегируем настройку отдельному модулю

    logging.info("🔧 Инициализация компонентов...")

    history = ChatHistory()
    client = AIClient()
    session = ChatSession(client, history)

    session.run()


if __name__ == "__main__":
    main()