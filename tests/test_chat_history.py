import pytest
from src.chat_history import ChatHistory


@pytest.fixture
def temp_db(tmp_path):
    """Создает временную БД для каждого теста, чтобы не мусорить"""
    return str(tmp_path / "test_history.json")


def test_add_message_increments_list(temp_db):
    history = ChatHistory(file_path=temp_db, max_messages=10)
    assert len(history.messages) == 0

    history.add_message("user", "Привет")
    assert len(history.messages) == 1
    assert history.messages[0]["content"] == "Привет"


def test_get_context_limits_messages(temp_db):
    # Создаем историю с лимитом 2
    history = ChatHistory(file_path=temp_db, max_messages=2)
    history.add_message("user", "1")
    history.add_message("user", "2")
    history.add_message("user", "3")

    # Должен вернуть только последние 2
    context = history.get_context()
    assert len(context) == 2
    assert context[0]["content"] == "2"


def test_clear_resets_history(temp_db):
    history = ChatHistory(file_path=temp_db, max_messages=10)
    history.add_message("user", "Тест")
    assert len(history.messages) == 1

    history.clear()
    assert len(history.messages) == 0


def test_corrupted_json_resets_gracefully(temp_db):
    # Пишем "мусор" в файл
    with open(temp_db, "w", encoding="utf-8") as f:
        f.write("THIS IS NOT JSON!!!")

    # Инициализация должна пройти без ошибки, создав пустой список
    history = ChatHistory(file_path=temp_db, max_messages=10)
    assert len(history.messages) == 0