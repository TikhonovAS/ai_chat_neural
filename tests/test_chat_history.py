import pytest
import json
from pathlib import Path
from src.chat_history import ChatHistory

# Р¤РёРєСЃС‚СѓСЂР°: СЃРѕР·РґР°РµРј РІСЂРµРјРµРЅРЅС‹Р№ С„Р°Р№Р» РґР»СЏ РєР°Р¶РґРѕРіРѕ С‚РµСЃС‚Р° Рё СѓРґР°Р»СЏРµС‚ РїРѕСЃР»Рµ
@pytest.fixture
def temp_history_file(tmp_path):
    """Р’РѕР·РІСЂР°С‰Р°РµС‚ РїСѓС‚СЊ Рє РІСЂРµРјРµРЅРЅРѕРјСѓ С„Р°Р№Р»Сѓ РёСЃС‚РѕСЂРёРё"""
    return tmp_path / "test_history.json"


class TestChatHistorySaleLoad:
    """РўРµСЃС‚С‹ СЃРѕС…СЂР°РЅРµРЅРёСЏ Рё Р·Р°РіСЂСѓР·РєРё РёСЃС‚РѕСЂРёРё"""

    def test_add_message_saves_immediately(self, temp_history_file):
        """РџСЂРѕРІРµСЂРєР° РїРѕСЃР»Рµ add_message С„Р°Р№Р» СЃСЂР°Р·Сѓ РѕР±РЅРѕРІР»СЏРµС‚СЃСЏ"""
        history = ChatHistory(filepath=temp_history_file)
        history.add_message("user", "РџСЂРёРІРµС‚!")

        # Р§РёС‚Р°РµРј С„Р°Р№Р» РІСЂСѓС‡РЅСѓСЋ
        with open(temp_history_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["role"] == "user"
        assert data[0]["content"] == "РџСЂРёРІРµС‚!"
        assert "timestamp" in data[0]   # РјРµС‚РєР° РІСЂРµРјРµРЅРё РґРѕР±Р°РІРёР»Р°СЃСЊ

    def test_load_nonexistent_file_starts_empty(self, temp_history_file):
        """РџСЂРѕРІРµСЂРєР°: РµСЃР»Рё С„Р°Р№Р»Р° РЅРµС‚, РёСЃС‚РѕСЂРёСЏ РїСѓСЃС‚Р° (РЅРµ РїР°РґР°РµС‚)"""
        # Р¤Р°Р№Р» РµС‰Рµ РЅРµ СЃРѕР·РґР°РЅ
        history = ChatHistory(filepath=temp_history_file)
        assert history.messages == []

    def test_load_corrupted_file_resets(self, temp_history_file):
        """РџСЂРѕРІРµСЂРєР°: Р±РёС‚С‹Р№ JSON РЅРµ Р»РѕРјР°РµС‚ РїСЂРѕРіСЂР°РјРјСѓ, Р° СЃР±СЂР°СЃС‹РІР°РµС‚ РёСЃС‚РѕСЂРёСЋ"""
        # РЎРѕР·РґР°РµРј "Р±РёС‚С‹Р№" С„Р°Р№Р»
        with open(temp_history_file, "w", encoding="utf-8") as f:
            f.write("{ РЅРµРІР°Р»РёРґРЅС‹Р№ json }")

        # РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ РЅРµ РґРѕР»Р¶РЅР° СѓРїР°СЃС‚СЊ
        history = ChatHistory(filepath=temp_history_file)
        assert history.messages == []   # РќР°С‡Р°Р» СЃ С‡РёСЃС‚РѕРіРѕ Р»РёСЃС‚Р°
        # Р С„Р°Р№Р» РїРµСЂРµР·Р°РїРёСЃР°РЅ РєРѕСЂСЂРµРєС‚РЅРѕ
        assert temp_history_file.exists()


class TestChatHistoryContext:
    """РўРµСЃС‚С‹ СЂР°Р±РѕС‚С‹ СЃ РєРѕРЅС‚РµРєСЃС‚РѕРј"""

    def test_get_context_limits_messages(self, temp_history_file):
        """РџСЂРѕРІРµСЂРєР°: get_context РІРѕР·РІСЂР°С‰Р°РµС‚ РЅРµ Р±РѕР»СЊС€Рµ N СЃРѕРѕР±С‰РµРЅРёР№"""
        history = ChatHistory(filepath=temp_history_file)

        # Р”РѕР±Р°РІР»СЏРµРј 15 СЃРѕРѕР±С‰РµРЅРёР№
        for i in range(15):
            history.add_message("user", f"РЎРѕРѕР±С‰РµРЅРёРµ {i}")

        # Р—Р°РїСЂР°С€РёРІР°РµРј РєРѕРЅС‚РµРєСЃС‚ РёР· 5 СЃРѕРѕР±С‰РµРЅРёР№
        context = history.get_context(max_messages=5)

        assert len(context) == 5
        # РџРѕСЃР»РµРґРЅРёРµ 5: РёРЅРґРµРєСЃС‹ 10-14
        assert context[0]["content"] == "РЎРѕРѕР±С‰РµРЅРёРµ 10"
        assert context[-1]["content"] == "РЎРѕРѕР±С‰РµРЅРёРµ 14"

    def test_clear_removes_all(self, temp_history_file):
        """РџСЂРѕРІРµСЂРєР°: clear() РїРѕР»РЅРѕСЃС‚СЊСЋ РѕС‡РёС‰Р°СЋС‚ РёСЃС‚РѕСЂРёСЋ"""
        history = ChatHistory(filepath=temp_history_file)
        history.add_message("user", "РўРµСЃС‚")
        history.clear()

        assert history.messages == []
        # Р С„Р°Р№Р» РЅР° РґРёСЃРєРµ С‚РѕР¶Рµ РїСѓСЃС‚
        with open(temp_history_file, "r", encoding="utf-8") as f:
            assert json.load(f) == []
