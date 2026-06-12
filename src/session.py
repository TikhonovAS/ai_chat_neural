import logging
from src.api_client import AIClient
from src.chat_history import ChatHistory

logger = logging.getLogger(__name__)


class ChatSession:
    """
    Контроллер диалога. Управляет циклом ввода, обработкой команд,
    вызовом ИИ и обновлением истории.
    """

    def __init__(self, client: AIClient, history: ChatHistory):
        self.client = client
        self.history = history

    def run(self) -> None:
        """Запускает основной цикл интерактивного диалога"""
        logger.info("🚀 Сессия диалога запущена")
        print("🤖 Бот готов! Введи /exit для выхода, /clear для очистки.")

        while True:
            try:
                user_input = input("\n👤 Ты: ").strip()
            except (EOFError, KeyboardInterrupt):
                logger.info("👋 Сессия прервана пользователем")
                print("\n👋 До встречи!")
                break

            if not user_input:
                continue

            if user_input.lower() in ["/exit", "exit", "/выход"]:
                logger.info("👋 Пользователь завершил сессию")
                print("👋 До встречи!")
                break

            if user_input.lower() == "/clear":
                self.history.clear()
                logger.info("🧹 История очищена пользователем")
                print("🧹 История очищена.")
                continue

            # 🔹 Передаём управление приватному методу обработки
            self._process_user_message(user_input)

    def _process_user_message(self, user_input: str) -> None:
        """Логика обработки одного шага диалога"""
        # 1. Сохраняем ввод пользователя
        self.history.add_message("user", user_input)
        logger.debug(f"📥 Пользователь: '{user_input}'")

        # 2. Формируем контекст
        context = self.history.get_context(max_messages=10)
        print("⏳ Думаю...")

        # 3. Запрашиваем ответ у ИИ
        answer = self.client.get_response(context)
        print(f"💡 Бот: {answer}")
        logger.info(f"📤 Бот: {answer[:60]}...")

        # 4. Сохраняем ответ бота
        self.history.add_message("assistant", answer)