import pytest
from unittest.mock import patch, MagicMock
from src.session import ChatSession
from src.api_client import AIClient
from src.chat_history import ChatHistory


class TestChatSession:
    """РўРµСЃС‚С‹ РєРѕРЅС‚СЂРѕР»Р»РµСЂР° РґРёР°Р»РѕРіР°. РџСЂРѕРІРµСЂСЏСЋС‚ Р»РѕРіРёРєСѓ РєРѕРјР°РЅРґ Рё РїРѕС‚РѕРє РґР°РЅРЅС‹С…."""

    @pytest.fixture
    def mocks(self):
        """РЎРѕР·РґР°С‘С‚ РёР·РѕР»РёСЂРѕРІР°РЅРЅС‹Рµ РјРѕРє-РѕР±СЉРµРєС‚С‹ РґР»СЏ РљР»РёРµРЅС‚Р° Рё РСЃС‚РѕСЂРёРё"""
        # 1. РњРѕРє РР-РєР»РёРµРЅС‚Р°: РІСЃРµРіРґР° РІРѕР·РІСЂР°С‰Р°РµС‚ РѕРґРёРЅ РѕС‚РІРµС‚
        client = MagicMock(spec=AIClient)
        client.get_response.return_value = "рџ¤– РўРµСЃС‚РѕРІС‹Р№ РѕС‚РІРµС‚ РР"

        # 2. РњРѕРє РСЃС‚РѕСЂРёРё: РІРѕР·РІСЂР°С‰Р°РµС‚ РїСѓСЃС‚РѕР№ РєРѕРЅС‚РµРєСЃС‚, С‡С‚РѕР±С‹ РЅРµ Р»РѕРјР°С‚СЊ С†РёРєР»
        history = MagicMock(spec=ChatHistory)
        history.get_context.return_value = [{"role": "user", "content": "С‚РµСЃС‚"}]

        return client, history

    def test_normal_flow_processes_message(self, mocks):
        """РџСЂРѕРІРµСЂРєР°: РѕР±С‹С‡РЅРѕРµ СЃРѕРѕР±С‰РµРЅРёРµ СЃРѕС…СЂР°РЅСЏРµС‚СЃСЏ РІ РёСЃС‚РѕСЂРёСЋ Рё РІС‹Р·С‹РІР°РµС‚ РР"""
        client, history = mocks
        session = ChatSession(client, history)

        # РРјРёС‚РёСЂСѓРµРј РІРІРѕРґ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ: СЃРѕРѕР±С‰РµРЅРёРµ в†’ РІС‹С…РѕРґ
        with patch("builtins.input", side_effect=["РџСЂРёРІРµС‚, Р±РѕС‚!", "/exit"]):
            session.run()

        # РџСЂРѕРІРµСЂСЏРµРј, С‡С‚Рѕ РєР»РёРµРЅС‚ Р±С‹Р» РІС‹Р·РІР°РЅ СЃ РєРѕРЅС‚РµРєСЃС‚РѕРј
        client.get_response.assert_called_once()
        # РџСЂРѕРІРµСЂСЏРµРј, С‡С‚Рѕ РёСЃС‚РѕСЂРёСЏ РѕР±РЅРѕРІРёР»Р°СЃСЊ РґРІР°Р¶РґС‹ (user + assistant)
        history.add_message.assert_any_call("user", "РџСЂРёРІРµС‚, Р±РѕС‚!")
        history.add_message.assert_any_call("assistant", "рџ¤– РўРµСЃС‚РѕРІС‹Р№ РѕС‚РІРµС‚ РР")

    def test_clear_command_resets_history(self, mocks):
        """РџСЂРѕРІРµСЂРєР°: РєРѕРјР°РЅРґР° /clear РІС‹Р·С‹РІР°РµС‚ РјРµС‚РѕРґ РѕС‡РёСЃС‚РєРё"""
        client, history = mocks
        session = ChatSession(client, history)

        # Р’РІРѕРґ: СЃРѕРѕР±С‰РµРЅРёРµ в†’ РѕС‡РёСЃС‚РєР° в†’ РІС‹С…РѕРґ
        with patch("builtins.input", side_effect=["РўРµСЃС‚", "/clear", "/exit"]):
            session.run()

        # РЈР±РµР¶РґР°РµРјСЃСЏ, С‡С‚Рѕ clear() Р±С‹Р» РІС‹Р·РІР°РЅ СЂРѕРІРЅРѕ 1 СЂР°Р·
        history.clear.assert_called_once()

    def test_empty_input_doesnt_break_flow(self, mocks):
        """РџСЂРѕРІРµСЂРєР°: РїСѓСЃС‚РѕР№ РІРІРѕРґ (РїСЂРѕР±РµР»/Enter) РёРіРЅРѕСЂРёСЂСѓРµС‚СЃСЏ, С†РёРєР» РїСЂРѕРґРѕР»Р¶Р°РµС‚СЃСЏ"""
        client, history = mocks
        session = ChatSession(client, history)

        # Р’РІРѕРґ: РїСЂРѕР±РµР» в†’ СЃРѕРѕР±С‰РµРЅРёРµ в†’ РІС‹С…РѕРґ
        with patch("builtins.input", side_effect=["   ", "Р Р°Р±РѕС‚Р°СЋ", "/exit"]):
            session.run()

        # РСЃС‚РѕСЂРёСЏ РґРѕР»Р¶РЅР° РѕР±РЅРѕРІРёС‚СЊСЃСЏ С‚РѕР»СЊРєРѕ РґР»СЏ "Р Р°Р±РѕС‚Р°СЋ", РїСЂРѕР±РµР» РёРіРЅРѕСЂРёСЂСѓРµС‚СЃСЏ
        assert history.add_message.call_count == 2  # user + assistant
        history.add_message.assert_any_call("user", "Р Р°Р±РѕС‚Р°СЋ")

    def test_keyboard_interrupt_exits_gracefully(self, mocks):
        """РџСЂРѕРІРµСЂРєР°: Ctrl+C (KeyboardInterrupt) РєРѕСЂСЂРµРєС‚РЅРѕ Р·Р°РІРµСЂС€Р°РµС‚ СЃРµСЃСЃРёСЋ"""
        client, history = mocks
        session = ChatSession(client, history)

        # РРјРёС‚РёСЂСѓРµРј РїСЂРµСЂС‹РІР°РЅРёРµ СЃСЂР°Р·Сѓ РїРѕСЃР»Рµ СЃС‚Р°СЂС‚Р°
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            session.run()  # РќРµ РґРѕР»Р¶РЅРѕ СѓРїР°СЃС‚СЊ СЃ traceback

        # РџСЂРѕРІРµСЂСЏРµРј, С‡С‚Рѕ РїСЂРё РІС‹С…РѕРґРµ РЅРёС‡РµРіРѕ РЅРµ СЃР»РѕРјР°Р»РѕСЃСЊ
        assert True  # Р•СЃР»Рё РґРѕС€Р»Рё СЃСЋРґР° в†’ С‚РµСЃС‚ РїСЂРѕР№РґРµРЅ