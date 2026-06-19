import json
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from config import WEB_DIR, DEFAULT_OLLAMA_HOST
from models import ChatRequest
from ollama_client import check_ollama_status
from chat_handler import stream_ollama
from html_pages import get_status_page


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
    
    @app.get("/api/health")
    async def health(ollama_host: str = DEFAULT_OLLAMA_HOST):
        """
        Проверка статуса подключения к Ollama.
        
        Возвращает:
        - 200 OK: Ollama доступен
        - 500 Internal Server Error: Ollama недоступен
        """
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
    
    @app.post("/api/chat")
    async def chat(req: ChatRequest):
        status_data = await check_ollama_status(DEFAULT_OLLAMA_HOST)
        
        if not status_data["reachable"]:
            error_msg = status_data.get("error", "Ollama is not reachable")
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
        
        messages = [{"role": "user", "content": req.message}]
        
        async def generate_ollama():
            async for event in stream_ollama(
                messages,
                DEFAULT_OLLAMA_HOST,
                ollama_model
            ):
                yield f"data: {json.dumps(event)}\n\n"
        
        return StreamingResponse(
            generate_ollama(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )
    
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