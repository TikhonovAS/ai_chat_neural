import requests
import time
from src.config import Settings

# -------------------------------------------------
# Р”РѕР±Р°РІР»РµРЅРѕ РїРѕСЃР»Рµ СЃРѕР·РґР°РЅРёСЏ РјРѕРґСѓР»СЏ logger.py рџ”»

import logging

# РџРѕР»СѓС‡Р°РµРј Р»РѕРіРіРµСЂ СЃ РёРјРµРЅРµРј "src.api.client"
logger = logging.getLogger(__name__)


# Р”РѕР±Р°РІР»РµРЅРѕ РїРѕСЃР»Рµ СЃРѕР·РґР°РЅРёСЏ РјРѕРґСѓР»СЏ logger.py рџ”є
# --------------------------------------------------

class AIClient:
    """
    РЈРЅРёРІРµСЂСЃР°Р»СЊРЅС‹Р№ РР-РєР»РёРµРЅС‚. РџРѕРґРґРµСЂР¶РёРІР°РµС‚: Р·Р°РіР»СѓС€РєСѓ, Hugging Face, OpenRouter.
    РђРІС‚РѕРјР°С‚РёС‡РµСЃРєРё РІС‹Р±РёСЂР°РµС‚ РїСЂРѕРІР°Р№РґРµСЂР° РїРѕ Settings.AI_PROVIDER.
    """

    def __init__(self):
        self.debug = Settings.DEBUG_MODE
        self.provider = Settings.AI_PROVIDER

    def get_response(self, messages: list[dict]) -> str:
        """
        РћС‚РїСЂР°РІР»СЏРµС‚ РљРћРќРўР•РљРЎРў РґРёР°Р»РѕРіР° РІ РЅРµР№СЂРѕСЃРµС‚СЊ Рё РІРѕР·РІСЂР°С‰Р°РµС‚ РѕС‚РІРµС‚.
        :param messages: СЃРїРёСЃРѕРє [{"role": "user/assistant", "content": "..."}]
        """
        # 1. Р—Р°РіР»СѓС€РєР° (РґР»СЏ СЂР°Р·СЂР°Р±РѕС‚РєРё Р±РµР· С‚СЂР°С‚С‹ Р»РёРјРёС‚РѕРІ)
        if self.debug:
            time.sleep(0.5)
            # РРјРёС‚РёСЂСѓРµРј, С‡С‚Рѕ РР Р°РЅР°Р»РёР·РёСЂСѓРµС‚ РёСЃС‚РѕСЂРёСЋ
            user_msgs = [m for m in messages if m["role"] == "user"]
            if not user_msgs:
                return "рџ§Є [MOCK] РСЃС‚РѕСЂРёСЏ РїСѓСЃС‚Р°."

            if len(messages) > 2:
                return f"рџ§Є [MOCK-РєРѕРЅС‚РµРєСЃС‚]\nР’РёР¶Сѓ {len(messages)} СЃРѕРѕР±С‰РµРЅРёР№.\nРџРѕСЃР»РµРґРЅРµРµ РѕС‚ С‚РµР±СЏ: {user_msgs[-1]['content']}"
            return f"рџ§Є [MOCK] РџРѕР»СѓС‡РµРЅРѕ: '{user_msgs[-1]['content']}'"

        # 2. РњР°СЂС€СЂСѓС‚РёР·Р°С†РёСЏ Р·Р°РїСЂРѕСЃР°
        if self.provider == "hf":
            return self._request_hf(messages)
        elif self.provider == "groq":
            return self._request_groq(messages)
        elif self.provider == "ollama":
            return self._request_ollama(messages)
        elif self.provider == "openrouter":
            return self._request_openrouter(messages)
        else:
            return f"вљ пёЏ РќРµРёР·РІРµСЃС‚РЅС‹Р№ РїСЂРѕРІР°Р№РґРµСЂ: {self.provider}"

    def _request_hf(self, messages: list[dict]) -> str:
        """Р—Р°РїСЂРѕСЃ Рє Hugging Face Inference API СЃ РїРѕР»РЅРѕР№ РёСЃС‚РѕСЂРёРµР№"""
        headers = {
            "Authorization": f"Bearer {Settings.HF_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": Settings.DEFAULT_MODEL,
            "messages": messages,  # вњ… РџРµСЂРµРґР°С‘Рј Р’Р•РЎР¬ СЃРїРёСЃРѕРє, Р° РЅРµ РѕРґРЅРѕ СЃРѕРѕР±С‰РµРЅРёРµ
            "max_tokens": 256
        }

        try:
            response = requests.post(
                Settings.HF_API_URL,
                headers=headers,
                json=payload,
                timeout=20
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            logger.warning("вЏі РўР°Р№РјР°СѓС‚ Р·Р°РїСЂРѕСЃР° Рє API (20 СЃРµРє)")
            return "вЏі РўР°Р№РјР°СѓС‚: РЅРµР№СЂРѕСЃРµС‚СЊ РЅРµ РѕС‚РІРµС‚РёР»Р° Р·Р° 20 СЃРµРєСѓРЅРґ."
        except requests.exceptions.HTTPError as e:
            logger.error(f"рџљЁ HTTP РћС€РёР±РєР° API: {e.response.status_code} | {e.response.text[:100]}")
            return f"рџљЁ РћС€РёР±РєР° API: {e.response.status_code} - {e.response.text[:100]}"
        except Exception as e:
            logger.exception(f"вљ пёЏ РќРµРѕР¶РёРґР°РЅРЅР°СЏ РѕС€РёР±РєР° РІ _request_hf")  # exception() Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё РїРёС€РµС‚ С‚СЂРµР№СЃР±РµРє
            return f"вљ пёЏ РќРµРѕР¶РёРґР°РЅРЅР°СЏ РѕС€РёР±РєР°: {str(e)}"

    def _request_groq(self, messages):
        """
        Р—Р°РїСЂРѕСЃ Рє Groq API.
        Р¤РѕСЂРјР°С‚ РёРґРµРЅС‚РёС‡РµРЅ OpenAI, РїРѕСЌС‚РѕРјСѓ payload Рё РїР°СЂСЃРёРЅРі РїРѕС‡С‚Рё С‚Р°РєРёРµ Р¶Рµ.
        """
        headers = {
            "Authorization": f"Bearer {Settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": Settings.DEFAULT_MODEL,
            "messages": messages,  # РїРµСЂРµРґР°РµРј РІРµСЃСЊ РєРѕРЅС‚РµРєСЃС‚ РґРёР°Р»РѕРіР°
            "max_tokens": 256,
            "temperature": 0.7  # Groq С…РѕСЂРѕС€Рѕ СЂРµР°РіРёСЂСѓРµС‚ РЅР° С‚РµРјРїРµСЂР°С‚СѓСЂСѓ
        }
        try:
            response = requests.post(
                Settings.GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=15  # Groq РѕР±С‹С‡РЅРѕ РѕС‚РІРµС‡Р°РµС‚ Р·Р° < 1 СЃРµРє
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            logger.warning("РўР°Р№РјР°СѓС‚: Р·Р°РїСЂРѕСЃР° Рє Groq (15 СЃРµРє)")
            return "РўР°Р№РјР°СѓС‚: Groq РЅРµ РѕС‚РІРµС‚РёР» Р·Р° 15 СЃРµРєСѓРЅРґ."
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP РћС€РёР±РєР° Groq: {e.response.status_code}")
            status = e.response.status_code
            text = e.response.text[:150]
            return f"РћС€РёР±РєР° API Groq: {status} - {text}"
        except Exception as e:
            logger.exception("РќРµРѕР¶РёРґР°РЅРЅР°СЏ РѕС€РёР±РєР° РІ _request_groq")
            return f"РћС€РёР±РєР° Groq: {str(e)}"

    def _request_ollama(self, messages):
        """
        Р—Р°РїСЂРѕСЃ Рє Р»РѕРєР°Р»СЊРЅРѕРјСѓ Ollama С‡РµСЂРµР· OpenAI-СЃРѕРІРјРµСЃС‚РёРјС‹Р№ API.
        РќРµ С‚СЂРµР±СѓРµС‚ API-РєР»СЋС‡Р°, СЂР°Р±РѕС‚Р°РµС‚ РЅР° localhost:11434
        """
        headers = {"Content-Type": "application/json"}  # рџ”“ Р‘РµР· Р°РІС‚РѕСЂРёР·Р°С†РёРё

        payload = {
            "model": Settings.DEFAULT_MODEL,
            "messages": messages,
            "stream": False,  # вќ— Р’Р°Р¶РЅРѕ: РёРЅР°С‡Рµ РїСЂРёРґС‘С‚ РїРѕС‚РѕРє, Р° РЅРµ JSON
            "options": {
                "temperature": 0.7,
                "num_predict": 512  # РћРіСЂР°РЅРёС‡РёРІР°РµРј РґР»РёРЅСѓ РѕС‚РІРµС‚Р°
            }
        }

        try:
            response = requests.post(
                Settings.OLLAMA_API_URL,  # http://localhost:11434/v1/chat/completions
                headers=headers,
                json=payload,
                timeout=120  # Р›РѕРєР°Р»СЊРЅС‹Рµ РјРѕРґРµР»Рё РјРѕРіСѓС‚ В«СЂР°Р·РѕРіСЂРµРІР°С‚СЊСЃСЏВ»
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.ConnectionError:
            logger.error("рџ”Њ Ollama РЅРµ РѕС‚РІРµС‡Р°РµС‚ РЅР° localhost:11434")
            return "рџ”Њ РћС€РёР±РєР°: Ollama РЅРµ Р·Р°РїСѓС‰РµРЅ. Р’С‹РїРѕР»РЅРёС‚Рµ 'ollama serve' РёР»Рё РѕС‚РєСЂРѕР№С‚Рµ РїСЂРёР»РѕР¶РµРЅРёРµ."
        except requests.exceptions.Timeout:
            logger.warning("вЏі РўР°Р№РјР°СѓС‚ Р·Р°РїСЂРѕСЃР° Рє Ollama (120 СЃРµРє)")
            return "вЏі РўР°Р№РјР°СѓС‚: РјРѕРґРµР»СЊ РґСѓРјР°РµС‚ СЃР»РёС€РєРѕРј РґРѕР»РіРѕ."
        except KeyError as e:
            logger.error(f"рџ”‘ РћС€РёР±РєР° РїР°СЂСЃРёРЅРіР° РѕС‚РІРµС‚Р° Ollama: {e}")
            return f"вљ пёЏ РќРµРѕР¶РёРґР°РЅРЅС‹Р№ С„РѕСЂРјР°С‚ РѕС‚РІРµС‚Р° РѕС‚ Ollama: {e}"
        except Exception as e:
            logger.exception("вљ пёЏ РќРµРѕР¶РёРґР°РЅРЅР°СЏ РѕС€РёР±РєР° РІ _request_ollama")
            return f"вљ пёЏ РћС€РёР±РєР°: {str(e)}"

    def _request_openrouter(self, messages):
        """Р—Р°РіР»СѓС€РєР° РґР»СЏ OpenRouter (РёСЃРїСЂР°РІР»РµРЅ РѕС‚СЃС‚СѓРї Рё СЃРёРіРЅР°С‚СѓСЂР°)"""
        return "рџ”§ OpenRouter РїРѕРєР° РЅРµ РїРѕРґРєР»СЋС‡С‘РЅ. РСЃРїРѕР»СЊР·СѓР№ AI_PROVIDER=hf РёР»Рё DEBUG_MODE=true"
