from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None


class ChatCreate(BaseModel):
    name: Optional[str] = None


class ChatRename(BaseModel):
    name: str


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = datetime.now()
    parts: Optional[List[dict]] = None


class ChatSession(BaseModel):
    id: str
    name: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    messages: List[ChatMessage] = []