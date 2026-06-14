import pytest
from unittest.mock import patch
from src.api_client import AIClient
from src.config import Settings

# 🔑 Гарантируем, что DEBUG_MODE всегда True во время тестов
@pytest.fixture(autouse=True)
def force_debug_mode():
    with patch.object(Settings, "DEBUG_MODE", True):
        yield

def test_mock_returns_string():
    client = AIClient()
    response = client.get_response([{"role": "user", "content": "Hi"}])
    assert isinstance(response, str)
    assert "MOCK" in response

def test_mock_context_awareness():
    """Проверяет, что бот 'видит' последнее сообщение"""
    client = AIClient()
    messages = [
        {"role": "user", "content": "First"},
        {"role": "assistant", "content": "Second"},
        {"role": "user", "content": "TargetMessage"}
    ]
    response = client.get_response(messages)
    assert "TargetMessage" in response

def test_empty_messages_handling():
    """Не должно падать при пустом списке"""
    client = AIClient()
    response = client.get_response([])
    assert isinstance(response, str)

def test_long_context_truncation_display():
    """Проверяет, что длинное сообщение обрезается в превью"""
    client = AIClient()
    long_msg = "A" * 100
    response = client.get_response([{"role": "user", "content": long_msg}])
    assert len(response) < 200