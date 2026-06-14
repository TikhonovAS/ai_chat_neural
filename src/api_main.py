from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Добавляем корень проекта в путь, чтобы импорты работали
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_client import AIClient
from src.chat_history import ChatHistory

# 1. Инициализация приложения
app = FastAPI(title="AI Chat Neural API", version="1.0.0")

# 2. Модели данных (Pydantic) - это "схема" запроса и ответа
class ChatRequest(BaseModel):
    message: str  # Ожидаем поле message типа string

class ChatResponse(BaseModel):
    response: str
    history_length: int

# 3. Глобальные переменные для хранения состояния (упрощенно для урока 1)
# В продакшене лучше использовать lifespan или зависимости (Depends)
chat_history = ChatHistory()
ai_client = AIClient()

# 4. Эндпоинт (Точка входа)
@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """Принимает сообщение, отправляет ИИ, возвращает ответ"""

    # Сохраняем сообщение пользователя
    chat_history.add_message("user", request.message)

    # Получаем ответ от ИИ
    context = chat_history.get_context()
    ai_response = ai_client.get_response(context)

    # Сохраняем ответ бота
    chat_history.add_message("assistant", ai_response)

    # Возвращаем JSON-ответ
    return {
        "response": ai_response,
        "history_length": len(chat_history.messages)
    }