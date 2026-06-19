import json
import uuid
import os
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from config import WEB_DIR, DEFAULT_OLLAMA_HOST
from models import ChatRequest, ChatCreate, ChatRename, ChatSession, ChatMessage
from ollama_client import check_ollama_status
from chat_handler import stream_ollama
from html_pages import get_status_page

# Директория для сохранения чатов
CHATS_DIR = Path(__file__).parent / "chats"


def ensure_chats_dir():
    """Создаёт директорию для чатов, если её нет"""
    if not CHATS_DIR.exists():
        CHATS_DIR.mkdir(parents=True, exist_ok=True)


def save_chat_to_file(chat: ChatSession):
    """Сохраняет чат в файл"""
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


def load_chat_from_file(chat_id: str) -> ChatSession | None:
    """Загружает чат из файла"""
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
    """Загружает все чаты из директории"""
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
    """Удаляет файл чата"""
    file_path = CHATS_DIR / f"{chat_id}.json"
    if file_path.exists():
        file_path.unlink()


def create_app() -> FastAPI:
    app = FastAPI(
        title="BFElite",
        docs_url=None,
        redoc_url=None,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Загружаем все чаты из файлов
    chats: dict[str, ChatSession] = load_all_chats()
    
    # ------------------------------------------------------------------
    # GET /api/health
    # ------------------------------------------------------------------
    
    @app.get("/api/health")
    async def health(ollama_host: str = DEFAULT_OLLAMA_HOST):
        """Проверка статуса подключения к Ollama."""
        status_data = await check_ollama_status(ollama_host)
        
        if status_data.get("reachable", False):
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": "ok",
                    "ollama": status_data
                }
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": "error",
                    "message": "Ollama is not reachable",
                    "ollama": status_data
                }
            )
    
    # ------------------------------------------------------------------
    # Работа с чатами
    # ------------------------------------------------------------------
    
    @app.get("/api/chats")
    async def get_chats():
        """Получить список всех чатов"""
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "chats": [
                    {
                        "id": chat_id,
                        "name": chat.name,
                        "created_at": chat.created_at.isoformat(),
                        "updated_at": chat.updated_at.isoformat(),
                        "messages_count": len(chat.messages)
                    }
                    for chat_id, chat in sorted(
                        chats.items(),
                        key=lambda x: x[1].updated_at,
                        reverse=True
                    )
                ]
            }
        )
    
    @app.post("/api/chats")
    async def create_chat(req: ChatCreate):
        """Создать новый чат"""
        chat_id = str(uuid.uuid4())[:8]
        name = req.name or f"Чат {chat_id}"
        
        chat = ChatSession(
            id=chat_id,
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            messages=[]
        )
        chats[chat_id] = chat
        save_chat_to_file(chat)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "id": chat_id,
                "name": chat.name,
                "created_at": chat.created_at.isoformat(),
                "updated_at": chat.updated_at.isoformat()
            }
        )
    
    @app.get("/api/chats/{chat_id}")
    async def get_chat(chat_id: str):
        """Получить чат по ID"""
        if chat_id not in chats:
            # Пробуем загрузить из файла
            chat = load_chat_from_file(chat_id)
            if chat:
                chats[chat_id] = chat
            else:
                raise HTTPException(status_code=404, detail="Chat not found")
        
        chat = chats[chat_id]
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
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
        )
    
    @app.put("/api/chats/{chat_id}")
    async def rename_chat(chat_id: str, req: ChatRename):
        """Переименовать чат"""
        if chat_id not in chats:
            chat = load_chat_from_file(chat_id)
            if chat:
                chats[chat_id] = chat
            else:
                raise HTTPException(status_code=404, detail="Chat not found")
        
        chat = chats[chat_id]
        chat.name = req.name
        chat.updated_at = datetime.now()
        save_chat_to_file(chat)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "id": chat.id,
                "name": chat.name,
                "updated_at": chat.updated_at.isoformat()
            }
        )
    
    @app.delete("/api/chats/{chat_id}")
    async def delete_chat(chat_id: str):
        """Удалить чат"""
        if chat_id in chats:
            del chats[chat_id]
        
        delete_chat_file(chat_id)
        
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"status": "deleted"}
        )
    
    # ------------------------------------------------------------------
    # POST /api/chat
    # ------------------------------------------------------------------
    
    @app.post("/api/chat")
    async def chat(req: ChatRequest):
        """
        Отправить сообщение в чат.
        Если chat_id не указан, создаётся новый чат.
        """
        # Проверяем или создаём чат
        chat_id = req.chat_id
        if chat_id:
            if chat_id not in chats:
                # Пробуем загрузить из файла
                chat = load_chat_from_file(chat_id)
                if chat:
                    chats[chat_id] = chat
                else:
                    raise HTTPException(status_code=404, detail="Chat not found")
            chat = chats[chat_id]
        else:
            # Создаём новый чат
            chat_id = str(uuid.uuid4())[:8]
            chat = ChatSession(
                id=chat_id,
                name=f"Чат {chat_id}",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                messages=[]
            )
            chats[chat_id] = chat
        
        # Сохраняем сообщение пользователя
        user_message = ChatMessage(
            role="user",
            content=req.message,
            timestamp=datetime.now()
        )
        chat.messages.append(user_message)
        chat.updated_at = datetime.now()
        save_chat_to_file(chat)
        
        # Проверяем статус Ollama
        status_data = await check_ollama_status(DEFAULT_OLLAMA_HOST)
        
        if not status_data["reachable"]:
            error_msg = status_data.get("error", "Ollama is not reachable")
            error_message = ChatMessage(
                role="assistant",
                content=f"Ошибка: {error_msg}",
                timestamp=datetime.now()
            )
            chat.messages.append(error_message)
            chat.updated_at = datetime.now()
            save_chat_to_file(chat)
            
            async def generate_error():
                yield f"data: {json.dumps({'type': 'error', 'message': f'Cannot connect to Ollama: {error_msg}'})}\n\n"
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return StreamingResponse(
                generate_error(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                },
            )
        
        models = status_data.get("models", [])
        if not models:
            error_message = ChatMessage(
                role="assistant",
                content="Нет доступных моделей. Загрузите модель: ollama pull llama3.2",
                timestamp=datetime.now()
            )
            chat.messages.append(error_message)
            chat.updated_at = datetime.now()
            save_chat_to_file(chat)
            
            async def generate_no_model():
                yield f"data: {json.dumps({'type': 'error', 'message': 'No models available. Pull a model first: ollama pull llama3.2'})}\n\n"
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return StreamingResponse(
                generate_no_model(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                },
            )
        
        ollama_model = models[0]
        
        # Собираем историю сообщений
        messages = []
        for msg in chat.messages:
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})
        
        async def generate_ollama():
            full_response = ""
            async for event in stream_ollama(
                messages,
                DEFAULT_OLLAMA_HOST,
                ollama_model
            ):
                if event.get("type") == "text":
                    full_response += event.get("content", "")
                yield f"data: {json.dumps(event)}\n\n"
            
            # Сохраняем ответ ассистента
            if full_response:
                assistant_message = ChatMessage(
                    role="assistant",
                    content=full_response,
                    timestamp=datetime.now(),
                    parts=[{"type": "text", "content": full_response, "streaming": False}]
                )
                chat.messages.append(assistant_message)
                chat.updated_at = datetime.now()
                save_chat_to_file(chat)

            # А также при ошибках
            error_message = ChatMessage(
                role="assistant",
                content=f"Ошибка: {error_msg}",
                timestamp=datetime.now(),
                parts=[{"type": "text", "content": f"Ошибка: {error_msg}", "streaming": False}]
            )
        
        return StreamingResponse(
            generate_ollama(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )
    
    # ------------------------------------------------------------------
    # Статика и главная страница
    # ------------------------------------------------------------------
    
    static_path = WEB_DIR / "static"
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    
    styles_path = WEB_DIR / "styles"
    if styles_path.exists():
        app.mount("/styles", StaticFiles(directory=str(styles_path)), name="styles")
    
    @app.get("/")
    async def serve_index():
        return HTMLResponse(get_status_page())
    
    return app