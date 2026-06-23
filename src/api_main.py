from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_client import AIClient
from src.chat_history import ChatHistory

app = FastAPI(title="AI Chat Neural API", version="1.0.0")

# 🔹 Добавляем CORS (разрешаем запросы с любого источника в разработке)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажи конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Модели данных
class ChatRequest(BaseModel):
    message: str


class Message(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    response: str
    history: list[Message]  # 🔹 Возвращаем всю историю
    history_length: int


# Глобальные переменные (для урока 1; в продакшене — сессии/БД)
chat_history = ChatHistory()
ai_client = AIClient()

async def verify_api_key(x_api_key: str = Header(...)):
    """Проверяет API-ключ из заголовка"""
    if x_api_key != Settings.API_KEY:
        raise HTTPException(status_code=)

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """Принимает сообщение, отправляет ИИ, возвращает ответ + историю"""

    chat_history.add_message("user", request.message)
    context = chat_history.get_context()
    ai_response = ai_client.get_response(context)
    chat_history.add_message("assistant", ai_response)

    # 🔹 Формируем историю для ответа
    history_messages = [
        Message(role=msg["role"], content=msg["content"])
        for msg in chat_history.messages
    ]

    return {
        "response": ai_response,
        "history": history_messages,
        "history_length": len(chat_history.messages)
    }


# 🔹 Новый эндпоинт: очистка истории
@app.post("/clear")
async def clear_history():
    """Очищает историю диалога"""
    chat_history.clear()
    return {"status": "cleared", "message": "История очищена"}