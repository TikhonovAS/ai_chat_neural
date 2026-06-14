import logging
from src.api_client import AIClient
from src.chat_history import ChatHistory

logger = logging.getLogger(__name__)


class ChatSession:
    """Контроллер диалога: обрабатывает ввод, команды и поток данных."""

    def __init__(self, client: AIClient, history: ChatHistory):
        self.client = client
        self.history = history

    def run(self) -> None:
        """Запускает интерактивный цикл диалога."""
        logger.info("🚀 Сессия диалога запущена")
        print("🤖 Бот готов! Введи /exit для выхода, /clear для очистки.")

        while True:
            try:
                user_input = input("\n👤 Ты: ").strip()
            except (KeyboardInterrupt, EOFError):
                logger.info("👋 Пользователь завершил сессию (Ctrl+C/EOF)")
                print("\n👋 До встречи!")
                break

            if not user_input:
                continue

            if user_input.lower() == "/exit":
                logger.info("👋 Пользователь завершил сессию")
                print("👋 До встречи!")
                break

            if user_input.lower() == "/clear":
                self.history.clear()
                print("🗑 История диалога очищена.")
                continue

            self._process_message(user_input)

    def _process_message(self, text: str) -> None:
        """Отправляет запрос в ИИ и логирует ответ."""
        self.history.add_message("user", text)
        print("⏳ Думаю...")

        try:
            response = self.client.get_response(self.history.get_context())
            print(f"💡 Бот: {response}")
            self.history.add_message("assistant", response)
            logger.info(f"📤 Бот: {response[:50]}...")
        except Exception as e:
            error_msg = f"⚠️ Ошибка: {e}"
            print(error_msg)
            logger.error(error_msg, exc_info=True)