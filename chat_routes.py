import asyncio
import json
from datetime import datetime
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse, StreamingResponse

from config import DEFAULT_OLLAMA_HOST
from models import ChatRequest, ChatCreate, ChatRename, ChatMessage
from ollama_client import check_ollama_status
from chat_handler import stream_ollama
from chat_storage import (
    save_chat_to_file, load_chat_from_file, 
    load_all_chats, delete_chat_file, create_new_chat
)
from tool_runner import run_sherlock, scrape_website, detect_target


def register_chat_routes(app):    
    chats = load_all_chats()
        
    @app.get("/api/chats")
    async def get_chats():
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
        chat = create_new_chat(req.name)
        chats[chat.id] = chat
        save_chat_to_file(chat)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "id": chat.id,
                "name": chat.name,
                "created_at": chat.created_at.isoformat(),
                "updated_at": chat.updated_at.isoformat()
            }
        )
    
    @app.get("/api/chats/{chat_id}")
    async def get_chat(chat_id: str):
        if chat_id not in chats:
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
        if chat_id in chats:
            del chats[chat_id]
        
        delete_chat_file(chat_id)
        
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"status": "deleted"}
        )
    
    @app.post("/api/chat")
    async def chat(req: ChatRequest):
        chat_id = req.chat_id
        if chat_id:
            if chat_id not in chats:
                chat = load_chat_from_file(chat_id)
                if chat:
                    chats[chat_id] = chat
                else:
                    raise HTTPException(status_code=404, detail="Chat not found")
            chat = chats[chat_id]
        else:
            chat = create_new_chat()
            chats[chat.id] = chat
        
        target_type, target_value = detect_target(req.message)
        
        if target_type == "username" and target_value:
            return await handle_tool_request(
                chat, req.message, target_value,
                "search_username", run_sherlock,
                f"## Results for user @{target_value}",
                f"Searching for user @{target_value}..."
            )
        
        elif target_type == "url" and target_value:
            return await handle_scrape_request(chat, req.message, target_value)
        
        return await handle_ollama_request(chat, req.message)


async def handle_tool_request(chat, message, target_value, tool_name, tool_func, result_title, loading_msg):
    user_message = ChatMessage(
        role="user",
        content=message,
        timestamp=datetime.now()
    )
    chat.messages.append(user_message)
    chat.updated_at = datetime.now()
    save_chat_to_file(chat)
    
    tool_result = await tool_func(target_value)
    
    result_message = ChatMessage(
        role="assistant",
        content=f"{result_title}\n\n{tool_result}",
        timestamp=datetime.now(),
        parts=[{"type": "text", "content": f"{result_title}\n\n{tool_result}", "streaming": False}]
    )
    chat.messages.append(result_message)
    chat.updated_at = datetime.now()
    save_chat_to_file(chat)
    
    async def generate_result():
        yield f"data: {json.dumps({'type': 'tool_start', 'tool': tool_name, 'input': target_value})}\n\n"
        yield f"data: {json.dumps({'type': 'text', 'content': loading_msg})}\n\n"
        await asyncio.sleep(0.5)
        yield f"data: {json.dumps({'type': 'text', 'content': tool_result})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    
    return StreamingResponse(
        generate_result(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


async def handle_scrape_request(chat, message, url):
    user_message = ChatMessage(
        role="user",
        content=message,
        timestamp=datetime.now()
    )
    chat.messages.append(user_message)
    chat.updated_at = datetime.now()
    save_chat_to_file(chat)
    
    scraped_content = await scrape_website(url)
    
    analysis_prompt = f"""
Проанализируй содержимое сайта {url} и предоставь структурированную информацию:

Содержимое сайта:
{scraped_content}

Требования:
1. Нужно найти Фамилию, Имя, Отчество, если имеется
2. Нужно найти электронную почту
3. Нужно найти контактные данные
4. Нужно найти дату рождения
5. Нужно найти ссылки, которые ведут на социальные сети

Ответ предоставь на русском языке в структурированном виде, используя Markdown.
"""
    
    status_data = await check_ollama_status(DEFAULT_OLLAMA_HOST)
    
    if not status_data["reachable"]:
        result_message = ChatMessage(
            role="assistant",
            content=f"## Scraping results for: {url}\n\n{scraped_content}",
            timestamp=datetime.now(),
            parts=[{"type": "text", "content": f"## Scraping results for: {url}\n\n{scraped_content}", "streaming": False}]
        )
        chat.messages.append(result_message)
        chat.updated_at = datetime.now()
        save_chat_to_file(chat)
        
        async def generate_result():
            yield f"data: {json.dumps({'type': 'tool_start', 'tool': 'scrape_website', 'input': url})}\n\n"
            yield f"data: {json.dumps({'type': 'text', 'content': f'Scraping website {url}...'})}\n\n"
            await asyncio.sleep(0.5)
            yield f"data: {json.dumps({'type': 'text', 'content': scraped_content})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
        return StreamingResponse(
            generate_result(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )
    
    models = status_data.get("models", [])
    if not models:
        result_message = ChatMessage(
            role="assistant",
            content=f"## Scraping results for: {url}\n\n{scraped_content}",
            timestamp=datetime.now(),
            parts=[{"type": "text", "content": f"## Scraping results for: {url}\n\n{scraped_content}", "streaming": False}]
        )
        chat.messages.append(result_message)
        chat.updated_at = datetime.now()
        save_chat_to_file(chat)
        
        async def generate_result():
            yield f"data: {json.dumps({'type': 'tool_start', 'tool': 'scrape_website', 'input': url})}\n\n"
            yield f"data: {json.dumps({'type': 'text', 'content': f'Scraping website {url}...'})}\n\n"
            await asyncio.sleep(0.5)
            yield f"data: {json.dumps({'type': 'text', 'content': scraped_content})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
        return StreamingResponse(
            generate_result(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )
    
    ollama_model = models[0]
    
    messages = [
        {"role": "system", "content": "You are an AI assistant that analyzes website content and provides structured information."},
        {"role": "user", "content": analysis_prompt}
    ]
    
    analysis_message = ChatMessage(
        role="user",
        content=f"Analyze website: {url}",
        timestamp=datetime.now()
    )
    chat.messages.append(analysis_message)
    chat.updated_at = datetime.now()
    save_chat_to_file(chat)
    
    async def generate_analysis():
        yield f"data: {json.dumps({'type': 'tool_start', 'tool': 'scrape_website', 'input': url})}\n\n"
        yield f"data: {json.dumps({'type': 'text', 'content': f'Scraping website {url}...'})}\n\n"
        await asyncio.sleep(0.5)
        
        full_response = ""
        async for event in stream_ollama(
            messages,
            DEFAULT_OLLAMA_HOST,
            ollama_model,
            enable_tools=False
        ):
            if event.get("type") == "text":
                full_response += event.get("content", "")
            yield f"data: {json.dumps(event)}\n\n"
        
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
        
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    
    return StreamingResponse(
        generate_analysis(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


async def handle_ollama_request(chat, message):
    user_message = ChatMessage(
        role="user",
        content=message,
        timestamp=datetime.now()
    )
    chat.messages.append(user_message)
    chat.updated_at = datetime.now()
    save_chat_to_file(chat)
    
    status_data = await check_ollama_status(DEFAULT_OLLAMA_HOST)
    
    if not status_data["reachable"]:
        error_msg = status_data.get("error", "Ollama is not reachable")
        error_message = ChatMessage(
            role="assistant",
            content=f"Error: {error_msg}",
            timestamp=datetime.now(),
            parts=[{"type": "text", "content": f"Error: {error_msg}", "streaming": False}]
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
            content="No models available. Pull a model first: ollama pull llama3.2",
            timestamp=datetime.now(),
            parts=[{"type": "text", "content": "No models available. Pull a model first: ollama pull llama3.2", "streaming": False}]
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
    
    messages = []
    for msg in chat.messages:
        if msg.role in ("user", "assistant"):
            messages.append({"role": msg.role, "content": msg.content})
    
    async def generate_ollama():
        full_response = ""
        async for event in stream_ollama(
            messages,
            DEFAULT_OLLAMA_HOST,
            ollama_model,
            enable_tools=False
        ):
            if event.get("type") == "text":
                full_response += event.get("content", "")
            yield f"data: {json.dumps(event)}\n\n"
        
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
    
    return StreamingResponse(
        generate_ollama(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )