import requests
import time
from src.config import Settings

# -------------------------------------------------
# Добавлено после создания модуля logger.py 🔻

import logging

# Получаем логгер с именем "src.api.client"
logger = logging.getLogger(__name__)


# Добавлено после создания модуля logger.py 🔺
# --------------------------------------------------

class AIClient:
    """
    Универсальный ИИ-клиент. Поддерживает: заглушку, Hugging Face, OpenRouter.
    Автоматически выбирает провайдера по Settings.AI_PROVIDER.
    """

    def __init__(self):
        self.debug = Settings.DEBUG_MODE
        self.provider = Settings.AI_PROVIDER

    def get_response(self, messages: list[dict]) -> str:
        """
        Отправляет КОНТЕКСТ диалога в нейросеть и возвращает ответ.
        :param messages: список [{"role": "user/assistant", "content": "..."}]
        """
        # 1. Заглушка (для разработки без траты лимитов)
        if self.debug:
            time.sleep(0.5)
            # Имитируем, что ИИ анализирует историю
            user_msgs = [m for m in messages if m["role"] == "user"]
            if not user_msgs:
                return "🧪 [MOCK] История пуста."

            if len(messages) > 2:
                return f"🧪 [MOCK-контекст]\nВижу {len(messages)} сообщений.\nПоследнее от тебя: {user_msgs[-1]['content']}"
            return f"🧪 [MOCK] Получено: '{user_msgs[-1]['content']}'"

        # 2. Маршрутизация запроса
        if self.provider == "hf":
            return self._request_hf(messages)
        elif self.provider == "openrouter":
            return self._request_openrouter(messages)
        else:
            return f"⚠️ Неизвестный провайдер: {self.provider}"

    def _request_hf(self, messages: list[dict]) -> str:
        """Запрос к Hugging Face Inference API с полной историей"""
        headers = {
            "Authorization": f"Bearer {Settings.HF_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": Settings.DEFAULT_MODEL,
            "messages": messages,  # ✅ Передаём ВЕСЬ список, а не одно сообщение
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
            logger.warning("⏳ Таймаут запроса к API (20 сек)")
            return "⏳ Таймаут: нейросеть не ответила за 20 секунд."
        except requests.exceptions.HTTPError as e:
            logger.error(f"🚨 HTTP Ошибка API: {e.response.status_code} | {e.response.text[:100]}")
            return f"🚨 Ошибка API: {e.response.status_code} - {e.response.text[:100]}"
        except Exception as e:
            logger.exception(f"⚠️ Неожиданная ошибка в _request_hf")  # exception() автоматически пишет трейсбек
            return f"⚠️ Неожиданная ошибка: {str(e)}"

    def _request_openrouter(self, messages: list[dict]) -> str:
        """Заглушка для OpenRouter (исправлен отступ и сигнатура)"""
        return "🔧 OpenRouter пока не подключён. Используй AI_PROVIDER=hf или DEBUG_MODE=true"
