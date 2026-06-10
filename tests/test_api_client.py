import pytest
from unittest.mock import patch, MagicMock

import requests

from src.api_client import AIClient
from src.config import Settings


class TestAIClientMockMode:
    """Тесты режима заглушки (без реальных запросов)"""

    @pytest.fixture
    def mock_settings(self):
        """Временно включаем DEBUG_MODE для тестов"""
        original = Settings.DEBUG_MODE
        Settings.DEBUG_MODE = True
        yield
        Settings.DEBUG_MODE = original  # Возвращаем как было

    def test_get_response_returns_mock_in_debug(self, mock_settings):
        """Проверка: в DEBUG_MODE возвращается заглушка, не стучится в сеть"""
        client = AIClient()
        messages = [{"role": "user", "content": "Тест"}]

        answer = client.get_response(messages)

        assert "[MOCK]" in answer
        assert "Тест" in answer  # Видит наше сообщение

    def test_mock_context_awareness(self, mock_settings):
        """Проверка: заглушка «видит» количество сообщений в истории"""
        client = AIClient()
        messages = [
            {"role": "user", "content": "Привет"},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": "Как дела?"}
        ]

        answer = client.get_response(messages)

        assert "3 сообщений" in answer or "Вижу 3" in answer


class TestAIClientErrorHandling:
    """Тесты обработки ошибок (с моками внешних запросов)"""

    @patch("src.api_client.requests.post")
    def test_timeout_returns_friendly_message(self, mock_post):
        """Проверка: при таймауте пользователь видит понятное сообщение"""
        # ✅ Имитируем ИМЕННО сетевой таймаут, а не общую ошибку
        mock_post.side_effect = requests.exceptions.Timeout("Connection timed out")

        with patch.object(Settings, "DEBUG_MODE", False):
            with patch.object(Settings, "AI_PROVIDER", "hf"):
                client = AIClient()
                answer = client._request_hf([])

        # ✅ Проверяем точный текст, который возвращает блок except requests.exceptions.Timeout:
        assert "Таймаут" in answer and "20 секунд" in answer