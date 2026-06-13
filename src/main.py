import logging
from src.logger import setup_logging
from src.api_client import AIClient
from src.chat_history import ChatHistory
from src.session import ChatSession


def main():
    """РўРѕС‡РєР° РІС…РѕРґР°. РўРѕР»СЊРєРѕ РёРЅРёС†РёР°Р»РёР·Р°С†РёСЏ Рё Р·Р°РїСѓСЃРє."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("рџ”§ РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ РєРѕРјРїРѕРЅРµРЅС‚РѕРІ...")

    # РЎР±РѕСЂРєР° Р·Р°РІРёСЃРёРјРѕСЃС‚РµР№
    client = AIClient()
    history = ChatHistory()

    # Р—Р°РїСѓСЃРє СЃРµСЃСЃРёРё
    session = ChatSession(client=client, history=history)
    logger.info(f"рџ“‚ Р—Р°РіСЂСѓР¶РµРЅРѕ {len(history.messages)} СЃРѕРѕР±С‰РµРЅРёР№ РёР· РёСЃС‚РѕСЂРёРё")

    # РџРµСЂРµРґР°С‘Рј СѓРїСЂР°РІР»РµРЅРёРµ СЃРµСЃСЃРёРё
    session.run()


if __name__ == "__main__":
    main()