import logging
from src.logger import setup_logging
from src.api_client import AIClient
from src.chat_history import ChatHistory
from src.session import ChatSession


def main():
    """Точка входа. Только инициализация и запуск."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("🔧 Инициализация компонентов...")

    # Сборка зависимостей
    client = AIClient()
    history = ChatHistory()

    # Запуск сессии
    session = ChatSession(client=client, history=history)
    logger.info(f"📂 Загружено {len(history.messages)} сообщений из истории")

    # Передаём управление сессии
    session.run()


if __name__ == "__main__":
    main()