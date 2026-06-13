import pytest
from unittest.mock import patch, MagicMock

import requests

from src.api_client import AIClient
from src.config import Settings


class TestAIClientMockMode:
    """РўРµСЃС‚С‹ СЂРµР¶РёРјР° Р·Р°РіР»СѓС€РєРё (Р±РµР· СЂРµР°Р»СЊРЅС‹С… Р·Р°РїСЂРѕСЃРѕРІ)"""

    @pytest.fixture
    def mock_settings(self):
        """Р’СЂРµРјРµРЅРЅРѕ РІРєР»СЋС‡Р°РµРј DEBUG_MODE РґР»СЏ С‚РµСЃС‚РѕРІ"""
        original = Settings.DEBUG_MODE
        Settings.DEBUG_MODE = True
        yield
        Settings.DEBUG_MODE = original  # Р’РѕР·РІСЂР°С‰Р°РµРј РєР°Рє Р±С‹Р»Рѕ

    def test_get_response_returns_mock_in_debug(self, mock_settings):
        """РџСЂРѕРІРµСЂРєР°: РІ DEBUG_MODE РІРѕР·РІСЂР°С‰Р°РµС‚СЃСЏ Р·Р°РіР»СѓС€РєР°, РЅРµ СЃС‚СѓС‡РёС‚СЃСЏ РІ СЃРµС‚СЊ"""
        client = AIClient()
        messages = [{"role": "user", "content": "РўРµСЃС‚"}]

        answer = client.get_response(messages)

        assert "[MOCK]" in answer
        assert "РўРµСЃС‚" in answer  # Р’РёРґРёС‚ РЅР°С€Рµ СЃРѕРѕР±С‰РµРЅРёРµ

    def test_mock_context_awareness(self, mock_settings):
        """РџСЂРѕРІРµСЂРєР°: Р·Р°РіР»СѓС€РєР° В«РІРёРґРёС‚В» РєРѕР»РёС‡РµСЃС‚РІРѕ СЃРѕРѕР±С‰РµРЅРёР№ РІ РёСЃС‚РѕСЂРёРё"""
        client = AIClient()
        messages = [
            {"role": "user", "content": "РџСЂРёРІРµС‚"},
            {"role": "assistant", "content": "Hi"},
            {"role": "user", "content": "РљР°Рє РґРµР»Р°?"}
        ]

        answer = client.get_response(messages)

        assert "3 СЃРѕРѕР±С‰РµРЅРёР№" in answer or "Р’РёР¶Сѓ 3" in answer


class TestAIClientErrorHandling:
    """РўРµСЃС‚С‹ РѕР±СЂР°Р±РѕС‚РєРё РѕС€РёР±РѕРє (СЃ РјРѕРєР°РјРё РІРЅРµС€РЅРёС… Р·Р°РїСЂРѕСЃРѕРІ)"""

    @patch("src.api_client.requests.post")
    def test_timeout_returns_friendly_message(self, mock_post):
        """РџСЂРѕРІРµСЂРєР°: РїСЂРё С‚Р°Р№РјР°СѓС‚Рµ РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РІРёРґРёС‚ РїРѕРЅСЏС‚РЅРѕРµ СЃРѕРѕР±С‰РµРЅРёРµ"""
        # вњ… РРјРёС‚РёСЂСѓРµРј РРњР•РќРќРћ СЃРµС‚РµРІРѕР№ С‚Р°Р№РјР°СѓС‚, Р° РЅРµ РѕР±С‰СѓСЋ РѕС€РёР±РєСѓ
        mock_post.side_effect = requests.exceptions.Timeout("Connection timed out")

        with patch.object(Settings, "DEBUG_MODE", False):
            with patch.object(Settings, "AI_PROVIDER", "hf"):
                client = AIClient()
                answer = client._request_hf([])

        # вњ… РџСЂРѕРІРµСЂСЏРµРј С‚РѕС‡РЅС‹Р№ С‚РµРєСЃС‚, РєРѕС‚РѕСЂС‹Р№ РІРѕР·РІСЂР°С‰Р°РµС‚ Р±Р»РѕРє except requests.exceptions.Timeout:
        assert "РўР°Р№РјР°СѓС‚" in answer and "20 СЃРµРєСѓРЅРґ" in answer