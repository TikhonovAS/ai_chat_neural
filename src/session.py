import logging
from src.api_client import AIClient
from src.chat_history import ChatHistory

logger = logging.getLogger(__name__)


class ChatSession:
    """
    РљРѕРЅС‚СЂРѕР»Р»РµСЂ РґРёР°Р»РѕРіР°. РЈРїСЂР°РІР»СЏРµС‚ С†РёРєР»РѕРј РІРІРѕРґР°, РѕР±СЂР°Р±РѕС‚РєРѕР№ РєРѕРјР°РЅРґ,
    РІС‹Р·РѕРІРѕРј РР Рё РѕР±РЅРѕРІР»РµРЅРёРµРј РёСЃС‚РѕСЂРёРё.
    """

    def __init__(self, client: AIClient, history: ChatHistory):
        self.client = client
        self.history = history

    def run(self) -> None:
        """Р—Р°РїСѓСЃРєР°РµС‚ РѕСЃРЅРѕРІРЅРѕР№ С†РёРєР» РёРЅС‚РµСЂР°РєС‚РёРІРЅРѕРіРѕ РґРёР°Р»РѕРіР°"""
        logger.info("рџљЂ РЎРµСЃСЃРёСЏ РґРёР°Р»РѕРіР° Р·Р°РїСѓС‰РµРЅР°")
        print("рџ¤– Р‘РѕС‚ РіРѕС‚РѕРІ! Р’РІРµРґРё /exit РґР»СЏ РІС‹С…РѕРґР°, /clear РґР»СЏ РѕС‡РёСЃС‚РєРё.")

        while True:
            try:
                user_input = input("\nрџ‘¤ РўС‹: ").strip()
            except (EOFError, KeyboardInterrupt):
                logger.info("рџ‘‹ РЎРµСЃСЃРёСЏ РїСЂРµСЂРІР°РЅР° РїРѕР»СЊР·РѕРІР°С‚РµР»РµРј")
                print("\nрџ‘‹ Р”Рѕ РІСЃС‚СЂРµС‡Рё!")
                break

            if not user_input:
                continue

            if user_input.lower() in ["/exit", "exit", "/РІС‹С…РѕРґ"]:
                logger.info("рџ‘‹ РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ Р·Р°РІРµСЂС€РёР» СЃРµСЃСЃРёСЋ")
                print("рџ‘‹ Р”Рѕ РІСЃС‚СЂРµС‡Рё!")
                break

            if user_input.lower() == "/clear":
                self.history.clear()
                logger.info("рџ§№ РСЃС‚РѕСЂРёСЏ РѕС‡РёС‰РµРЅР° РїРѕР»СЊР·РѕРІР°С‚РµР»РµРј")
                print("рџ§№ РСЃС‚РѕСЂРёСЏ РѕС‡РёС‰РµРЅР°.")
                continue

            # рџ”№ РџРµСЂРµРґР°С‘Рј СѓРїСЂР°РІР»РµРЅРёРµ РїСЂРёРІР°С‚РЅРѕРјСѓ РјРµС‚РѕРґСѓ РѕР±СЂР°Р±РѕС‚РєРё
            self._process_user_message(user_input)

    def _process_user_message(self, user_input: str) -> None:
        """Р›РѕРіРёРєР° РѕР±СЂР°Р±РѕС‚РєРё РѕРґРЅРѕРіРѕ С€Р°РіР° РґРёР°Р»РѕРіР°"""
        # 1. РЎРѕС…СЂР°РЅСЏРµРј РІРІРѕРґ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ
        self.history.add_message("user", user_input)
        logger.debug(f"рџ“Ґ РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ: '{user_input}'")

        # 2. Р¤РѕСЂРјРёСЂСѓРµРј РєРѕРЅС‚РµРєСЃС‚
        context = self.history.get_context(max_messages=10)
        print("вЏі Р”СѓРјР°СЋ...")

        # 3. Р—Р°РїСЂР°С€РёРІР°РµРј РѕС‚РІРµС‚ Сѓ РР
        answer = self.client.get_response(context)
        print(f"рџ’Ў Р‘РѕС‚: {answer}")
        logger.info(f"рџ“¤ Р‘РѕС‚: {answer[:60]}...")

        # 4. РЎРѕС…СЂР°РЅСЏРµРј РѕС‚РІРµС‚ Р±РѕС‚Р°
        self.history.add_message("assistant", answer)