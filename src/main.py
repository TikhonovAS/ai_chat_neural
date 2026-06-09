import sys
import os

# -----------------------------------------------
# Вставили после создания модуля logger.py 🔻

import logging
from src.logger import setup_logging
from src.api_client import AIClient
from src.chat_history import ChatHistory

# Инициализировали логирование ДО всего остального кода
setup_logging()

# Получаем логгер для этого модуля
logger = logging.getLogger(__name__)

def main():
    logger.info ("Запуск AI Chat Neural Bot ...")  # Запись в файл и консоль
    client = AIClient()
    history = ChatHistory()
    logger.info(f"Загруженная история: {len(history.messages)} сообщений.")

    print("Бот готов! Введи /exit для выхода, /clear для очистки.")

    while True:
        try:
            user_input = input("\n Ты: ").strip()
        except (EOFError, KeyboardInterrupt):
            logger.info("Пользователь завершил сессию (Ctrl+C или EOF).")
            print("\nДо встречи!")
            break

        if not user_input:
            continue
        if user_input.lower() == "/exit":
            logger.info("Пользователь ввел команду /exit.")
            print("До встречи!")
            break
        if user_input.lower() == "/clear":
            history.clear()
            logger.info("История диалогов очищена пользователем.")
            print("История очищена.")
            continue

        history.add_message("user", user_input)
        logger.debug(f"Пользователь отправил: '{user_input}'")  # Не покажется в консоли, но сохранится в файл

        context = history.get_context(max_messages=10)
        print("Думаю ...")

        answer = client.get_response(context)
        print(f"Бот: {answer}")
        logger.info(f"Бот ответил: {answer[:50]} ...")  # Обрезал для лого, чтобы не забивать файл

        history.add_message("assistant", answer)

# Вставили после создания модуля logger.py 🔺
# -----------------------------------------------

# Добавляем корень проекта в пути импорта, чтобы Python видел папку src/
# Это стандартный патерн для src-layout проектов
sys.path.insert(0, os.path.dirname(__file__))

from src.chat_history import ChatHistory
from src.api_client import AIClient

if __name__ == "__main__":
    main()                           # 🔺🔻 Добавлен после создания модуля logger.py
    client = AIClient()
    history = ChatHistory()

    print("Бот готов! Введи / exit для выхода")
    while True:
        user_input = input("\nТы: ").strip()
        if user_input.lower() in ["/exit", "выход"]:
            break

        # 1. Добавляем сообщение пользователя в историю
        history.add_message("user", user_input)

        # 2. Берем КОНТЕКСТ (список словарей), а не строку
        context = history.get_context(max_messages=10)

        # 3. Передаем context, а не user_input
        print("Думаю ...")
        answer = client.get_response(context)

        # 4. Сохраняем ответ бота в историю
        history.add_message("assistant", answer)
        print(f"Бот: {answer}")
