import pytest
from unittest.mock import patch, MagicMock
from src.session import ChatSession
from src.api_client import AIClient
from src.chat_history import ChatHistory


class TestChatSession:
    """Тесты контроллера диалога. Проверяют логику команд и поток данных."""

    @pytest.fixture
    def mocks(self):
        """Создаёт изолированные мок-объекты для Клиента и Истории"""
        # 1. Мок ИИ-клиента: всегда возвращает один ответ
        client = MagicMock(spec=AIClient)
        client.get_response.return_value = "🤖 Тестовый ответ ИИ"

        # 2. Мок Истории: возвращает пустой контекст, чтобы не ломать цикл
        history = MagicMock(spec=ChatHistory)
        history.get_context.return_value = [{"role": "user", "content": "тест"}]

        return client, history

    def test_normal_flow_processes_message(self, mocks):
        """Проверка: обычное сообщение сохраняется в историю и вызывает ИИ"""
        client, history = mocks
        session = ChatSession(client, history)

        # Имитируем ввод пользователя: сообщение → выход
        with patch("builtins.input", side_effect=["Привет, бот!", "/exit"]):
            session.run()

        # Проверяем, что клиент был вызван с контекстом
        client.get_response.assert_called_once()
        # Проверяем, что история обновилась дважды (user + assistant)
        history.add_message.assert_any_call("user", "Привет, бот!")
        history.add_message.assert_any_call("assistant", "🤖 Тестовый ответ ИИ")

    def test_clear_command_resets_history(self, mocks):
        """Проверка: команда /clear вызывает метод очистки"""
        client, history = mocks
        session = ChatSession(client, history)

        # Ввод: сообщение → очистка → выход
        with patch("builtins.input", side_effect=["Тест", "/clear", "/exit"]):
            session.run()

        # Убеждаемся, что clear() был вызван ровно 1 раз
        history.clear.assert_called_once()

    def test_empty_input_doesnt_break_flow(self, mocks):
        """Проверка: пустой ввод (пробел/Enter) игнорируется, цикл продолжается"""
        client, history = mocks
        session = ChatSession(client, history)

        # Ввод: пробел → сообщение → выход
        with patch("builtins.input", side_effect=["   ", "Работаю", "/exit"]):
            session.run()

        # История должна обновиться только для "Работаю", пробел игнорируется
        assert history.add_message.call_count == 2  # user + assistant
        history.add_message.assert_any_call("user", "Работаю")

    def test_keyboard_interrupt_exits_gracefully(self, mocks):
        """Проверка: Ctrl+C (KeyboardInterrupt) корректно завершает сессию"""
        client, history = mocks
        session = ChatSession(client, history)

        # Имитируем прерывание сразу после старта
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            session.run()  # Не должно упасть с traceback

        # Проверяем, что при выходе ничего не сломалось
        assert True  # Если дошли сюда → тест пройден