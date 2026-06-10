import pytest
import json
from pathlib import Path
from src.chat_history import ChatHistory

# Фикстура: создаем временный файл для каждого теста и удаляет после
@pytest.fixture
def temp_history_file(tmp_path):
    """Возвращает путь к временному файлу истории"""
    return tmp_path / "test_history.json"


class TestChatHistorySaleLoad:
    """Тесты сохранения и загрузки истории"""

    def test_add_message_saves_immediately(self, temp_history_file):
        """Проверка после add_message файл сразу обновляется"""
        history = ChatHistory(filepath=temp_history_file)
        history.add_message("user", "Привет!")

        # Читаем файл вручную
        with open(temp_history_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["role"] == "user"
        assert data[0]["content"] == "Привет!"
        assert "timestamp" in data[0]   # метка времени добавилась

    def test_load_nonexistent_file_starts_empty(self, temp_history_file):
        """Проверка: если файла нет, история пуста (не падает)"""
        # Файл еще не создан
        history = ChatHistory(filepath=temp_history_file)
        assert history.messages == []

    def test_load_corrupted_file_resets(self, temp_history_file):
        """Проверка: битый JSON не ломает программу, а сбрасывает историю"""
        # Создаем "битый" файл
        with open(temp_history_file, "w", encoding="utf-8") as f:
            f.write("{ невалидный json }")

        # Инициализация не должна упасть
        history = ChatHistory(filepath=temp_history_file)
        assert history.messages == []   # Начал с чистого листа
        # И файл перезаписан корректно
        assert temp_history_file.exists()


class TestChatHistoryContext:
    """Тесты работы с контекстом"""

    def test_get_context_limits_messages(self, temp_history_file):
        """Проверка: get_context возвращает не больше N сообщений"""
        history = ChatHistory(filepath=temp_history_file)

        # Добавляем 15 сообщений
        for i in range(15):
            history.add_message("user", f"Сообщение {i}")

        # Запрашиваем контекст из 5 сообщений
        context = history.get_context(max_messages=5)

        assert len(context) == 5
        # Последние 5: индексы 10-14
        assert context[0]["content"] == "Сообщение 10"
        assert context[-1]["content"] == "Сообщение 14"

    def test_clear_removes_all(self, temp_history_file):
        """Проверка: clear() полностью очищают историю"""
        history = ChatHistory(filepath=temp_history_file)
        history.add_message("user", "Тест")
        history.clear()

        assert history.messages == []
        # И файл на диске тоже пуст
        with open(temp_history_file, "r", encoding="utf-8") as f:
            assert json.load(f) == []
