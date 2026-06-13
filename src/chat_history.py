import json
from pathlib import Path
from datetime import datetime


class ChatHistory:
    """
    РљР»Р°СЃСЃ РґР»СЏ С…СЂР°РЅРµРЅРёСЏ РґРёР°Р»РѕРіР°.
    РџРѕРґРґРµСЂР¶РёРІР°РµС‚: РґРѕР±Р°РІР»РµРЅРёРµ СЃРѕРѕР±С‰РµРЅРёР№, СЃРѕС…СЂР°РЅРµРЅРёРµ РІ JSON, Р·Р°РіСЂСѓР·РєСѓ
    """

    def __init__(self, filepath="history.json"):
        self.filepath = Path(filepath)
        self.messages = []
        self._load()

    def add_message(self, role, content):
        """Р”РѕР±Р°РІР»СЏРµС‚ СЃРѕРѕР±С‰РµРЅРёРµ РІ РёСЃС‚РѕСЂРёСЋ Рё СЃСЂР°Р·Сѓ СЃРѕС…СЂР°РЅРёСЏРµС‚ РЅР° РґРёСЃРє"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        self._save()

    def get_context(self, max_messages=10):
        """Р’РѕР·РІСЂР°С‰Р°РµС‚ РїРѕСЃР»РµРґРЅРёРµ N СЃРѕРѕР±С‰РµРЅРёР№ РґР»СЏ РѕС‚РїСЂР°РІРєРё РІ API"""
        return self.messages[-max_messages:]

    def clear(self):
        """РћС‡РёС‰Р°РµС‚ РёСЃС‚РѕСЂРёСЋ"""
        self.messages = []
        self._save()

    def _save(self):
        """Р’РЅСѓС‚СЂРµРЅРЅРёР№ РјРµС‚РѕРґ: СЃРѕС…СЂР°РЅСЏРµС‚ РёСЃС‚РѕСЂРёСЋ РІ JSON-С„Р°Р№Р»"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)

    def _load(self):
        """Р’РЅСѓС‚СЂРµРЅРЅРёР№ РјРµС‚РѕРґ: Р·Р°РіСЂСѓР¶Р°РµС‚ РёСЃС‚РѕСЂРёСЋ РёР· С„Р°Р№Р»Р°, РµСЃР»Рё РѕРЅ РµСЃС‚СЊ"""
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:  # Р¤Р°Р№Р» РїСѓСЃС‚РѕР№
                        self.messages = []
                        return
                    self.messages = json.loads(content)

            except json.JSONDecodeError:
                # Р•СЃР»Рё С„Р°Р№Р» РїРѕРІСЂРµР¶РґРµРЅ РёР»Рё РїСѓСЃС‚РѕР№, РЅР°С‡РёРЅР°РµРј СЃ РЅСѓР»СЏ
                print("history.json РїРѕРІСЂРµР¶РґРµРЅ. РќР°С‡РёРЅР°СЋ РЅРѕРІСѓСЋ РёСЃС‚РѕСЂРёСЋ.")
                self.messages = []
                self._save()  # РїРµСЂРµР·Р°РїРёСЃС‹РІР°РµРј С„Р°Р№Р» РєРѕСЂСЂРµРєС‚РЅС‹Рј РїСѓСЃС‚С‹Рј СЃРїРёСЃРєРѕРј

            except Exception as e:
                # Р›СЋР±РѕР№ РґСЂСѓРіРѕР№ С„Р°СЂСЃ-РјР°Р¶РѕСЂ (РїСЂР°РІР° РґРѕСЃС‚СѓРїР°, СЃР±РѕР№ РґРёСЃРєР°)
                print(f"РћС€РёР±РєР° Р·Р°РіСЂСѓР·РєРё РёСЃС‚РѕСЂРёРё: {e}. РќР°С‡РёРЅР°СЋ СЃ РЅСѓР»СЏ.")
                self.messages = []
