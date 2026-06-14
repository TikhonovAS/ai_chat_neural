import pytest
from unittest.mock import patch
from src.session import ChatSession
from src.chat_history import ChatHistory
from src.api_client import AIClient


@pytest.fixture
def session(tmp_path):
    """Собирает сессию с временной БД и Mock-клиентом"""
    db = tmp_path / "sess.json"
    history = ChatHistory(file_path=str(db))
    client = AIClient(provider="mock")
    return ChatSession(client=client, history=history)


def test_normal_flow_processes_message(session):
    # Имитируем ввод: "Привет" -> "/exit"
    with patch('builtins.input', side_effect=["Привет", "/exit"]):
        session.run()

    # Проверяем, что сообщение сохранилось (User + Bot ответ)
    assert len(session.history.messages) == 2


def test_clear_command_resets_history(session):
    session.history.add_message("user", "Old Data")

    # Вводим: /clear -> /exit
    with patch('builtins.input', side_effect=["/clear", "/exit"]):
        session.run()

    assert len(session.history.messages) == 0


def test_empty_input_doesnt_break_flow(session):
    # Вводим: "" (пусто) -> "/exit"
    with patch('builtins.input', side_effect=["", "/exit"]):
        session.run()

    # Сообщение не должно добавиться
    assert len(session.history.messages) == 0


def test_keyboard_interrupt_exits_gracefully(session):
    # Имитируем Ctrl+C
    with patch('builtins.input', side_effect=KeyboardInterrupt()):
        session.run()

    # Тест просто не должен упасть с ошибкой
    assert True