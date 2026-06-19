from pydantic import BaseModel


class ChatRequest(BaseModel):
    #Запрос к /api/chat - только message обязателен
    message: str