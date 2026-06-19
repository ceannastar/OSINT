import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import CHATS_DIR
from models import ChatSession, ChatMessage


def ensure_chats_dir():
    if not CHATS_DIR.exists():
        CHATS_DIR.mkdir(parents=True, exist_ok=True)


def save_chat_to_file(chat: ChatSession):
    ensure_chats_dir()
    file_path = CHATS_DIR / f"{chat.id}.json"
    
    data = {
        "id": chat.id,
        "name": chat.name,
        "created_at": chat.created_at.isoformat(),
        "updated_at": chat.updated_at.isoformat(),
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "parts": msg.parts or []
            }
            for msg in chat.messages
        ]
    }
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_chat_from_file(chat_id: str) -> Optional[ChatSession]:
    file_path = CHATS_DIR / f"{chat_id}.json"
    if not file_path.exists():
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    chat = ChatSession(
        id=data["id"],
        name=data["name"],
        created_at=datetime.fromisoformat(data["created_at"]),
        updated_at=datetime.fromisoformat(data["updated_at"]),
        messages=[]
    )
    
    for msg_data in data.get("messages", []):
        msg = ChatMessage(
            role=msg_data["role"],
            content=msg_data["content"],
            timestamp=datetime.fromisoformat(msg_data["timestamp"]),
            parts=msg_data.get("parts", [])
        )
        chat.messages.append(msg)
    
    return chat


def load_all_chats() -> dict[str, ChatSession]:
    ensure_chats_dir()
    chats = {}
    
    for file_path in CHATS_DIR.glob("*.json"):
        try:
            chat = load_chat_from_file(file_path.stem)
            if chat:
                chats[chat.id] = chat
        except Exception as e:
            print(f"Ошибка загрузки чата {file_path}: {e}")
    
    return chats


def delete_chat_file(chat_id: str):
    file_path = CHATS_DIR / f"{chat_id}.json"
    if file_path.exists():
        file_path.unlink()


def create_new_chat(name: Optional[str] = None) -> ChatSession:
    chat_id = str(uuid.uuid4())[:8]
    chat_name = name or f"Чат {chat_id}"
    
    chat = ChatSession(
        id=chat_id,
        name=chat_name,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        messages=[]
    )
    
    return chat