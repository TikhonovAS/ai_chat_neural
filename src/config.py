import os
from dotenv import load_dotenv

# Р—Р°РіСЂСѓР¶Р°РµРј РїРµСЂРµРјРµРЅРЅС‹Рµ РёР· .env РІ РѕРєСЂСѓР¶РµРЅРёРµ Python
# Р•СЃР»Рё .env РЅРµС‚ (РЅР°РїСЂРёРјРµСЂ, РІ CI/CD), load_dotenv РїСЂРѕСЃС‚Рѕ РїСЂРѕРёРіРЅРѕСЂРёСЂСѓРµС‚ С€Р°Рі
load_dotenv()


class Settings:
    """
    РљР»Р°СЃСЃ-С…СЂР°РЅРёР»РёС‰Рµ РЅР°СЃС‚СЂРѕРµРє РїСЂРѕРµРєС‚Р°.
    РђРЅР°Р»РѕРіРёСЏ: "РјРµРЅРµРґР¶РµСЂ СЃРµР№С„Р°" вЂ” РѕРЅ Р·РЅР°РµС‚, РіРґРµ Р»РµР¶Р°С‚ РєР»СЋС‡Рё Рё РјРѕРґРµР»Рё,
    РЅРѕ РЅРµ СЂР°СЃРєСЂС‹РІР°РµС‚ РёС… РЅР°РїСЂСЏРјСѓСЋ РІ Р»РѕРіРёРєРµ Р±РѕС‚Р°.
    """

    # Р‘РµСЂС‘Рј РєР»СЋС‡ РёР· РѕРєСЂСѓР¶РµРЅРёСЏ. Р•СЃР»Рё РµРіРѕ РЅРµС‚ вЂ” РІС‹Р·С‹РІР°РµРј РѕС€РёР±РєСѓ СЃСЂР°Р·Сѓ,
    # Р° РЅРµ Р»РѕРІРёРј РµС‘ РїРѕСЃРµСЂРµРґРёРЅРµ СЂР°Р±РѕС‚С‹ Р±РѕС‚Р°.
    # РџСЂРѕРІР°Р№РґРµСЂ: 'hf' (Hugging Face) / 'openrouter' / 'mock'
    AI_PROVIDER = os.getenv("AI_PROVIDER", "hf")

    # РљР»СЋС‡Рё
    HF_API_KEY = os.getenv("HF_API_KEY", "")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

    # URL API (Hugging Face РїРѕРґРґРµСЂР¶РёРІР°РµС‚ OpenAI-С„РѕСЂРјР°С‚)
    HF_API_URL = "https://api-inference.huggingface.co/v1/chat/completions"
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

    # РњРѕРґРµР»СЊ РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "Qwen/Qwen2.5-7B-Instruct")

    # Р РµР¶РёРј РѕС‚Р»Р°РґРєРё
    DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"

    # Р’Р°Р»РёРґР°С†РёСЏ РїСЂРё СЃС‚Р°СЂС‚Рµ
    if not DEBUG_MODE and AI_PROVIDER == "hf" and not HF_API_KEY:
        raise ValueError("HF_API_KEY РЅРµ РЅР°Р№РґРµРЅ РІ .env! РџРѕР»СѓС‡Рё РЅР° huggingface.co/setting/tokens")


    # РќР°СЃС‚СЂРѕР№РєРё Groq API
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

    # Р’Р°Р»РёРґР°С†РёСЏ РєР»СЋС‡Р° РїСЂРё СЃС‚Р°СЂС‚Рµ (РµСЃР»Рё РІС‹Р±СЂР°РЅ Grog Рё РІС‹РєР»СЋС‡РµРЅ BEBUG)
    if not DEBUG_MODE and AI_PROVIDER == "groq" and not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY РЅРµ РЅР°Р№РґРµРЅ РІ .env! РџРѕР»СѓС‡Рё Р±РµСЃРїР»Р°С‚РЅРѕ РЅР° console.groq.com/keys"
        )

    # рџ”№ РќР°СЃС‚СЂРѕР№РєРё Ollama (Р»РѕРєР°Р»СЊРЅС‹Р№ API, Р±РµР· РєР»СЋС‡Р°)
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/v1/chat/completions")

    # рџ”“ Ollama РЅРµ С‚СЂРµР±СѓРµС‚ API-РєР»СЋС‡Р°, РЅРѕ РјРѕР¶РЅРѕ РґРѕР±Р°РІРёС‚СЊ РІР°Р»РёРґР°С†РёСЋ РјРѕРґРµР»Рё
    if not DEBUG_MODE and AI_PROVIDER == "ollama":
        # РџСЂРѕРІРµСЂСЏРµРј, С‡С‚Рѕ РјРѕРґРµР»СЊ Р·Р°РґР°РЅР° (РЅРµ РїСѓСЃС‚Р°СЏ СЃС‚СЂРѕРєР°)
        if not DEFAULT_MODEL:
            raise ValueError(
                "DEFAULT_MODEL РЅРµ Р·Р°РґР°РЅ РґР»СЏ Ollama! РџСЂРёРјРµСЂ: 'llama3.2:3b'"
            )