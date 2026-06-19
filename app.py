from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from config import WEB_DIR, DEFAULT_OLLAMA_HOST, DEFAULT_OLLAMA_MODEL
from ollama_client import check_ollama_status
from html_pages import get_status_page
from chat_routes import register_chat_routes


class ModelChangeRequest(BaseModel):
    model: str


class TelegramConfig(BaseModel):
    api_id: str = ""
    api_hash: str = ""
    phone: str = ""


class VkConfig(BaseModel):
    token: str = ""


def update_env_file(env_path: Path, env_vars: dict) -> None:
    lines = []
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    updated_lines = []
    found_keys = set()
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            updated_lines.append(line)
            continue
        
        for key, value in env_vars.items():
            if line.startswith(f'{key}='):
                if value:
                    updated_lines.append(f'{key}={value}')
                else:
                    updated_lines.append(f'#{key}=')
                found_keys.add(key)
                break
        else:
            updated_lines.append(line)
    
    for key, value in env_vars.items():
        if key not in found_keys:
            if value:
                updated_lines.append(f'{key}={value}')
            else:
                updated_lines.append(f'#{key}=')
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(updated_lines) + '\n')


def get_env_value(env_path: Path, key: str) -> str:
    if not env_path.exists():
        return ""
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith(f'{key}='):
                return line.split('=', 1)[1].strip()
    return ""


def create_app() -> FastAPI:
    app = FastAPI(
        title="BFElite",
        docs_url=None,
        redoc_url=None,
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    register_chat_routes(app)
    
    env_path = Path(__file__).parent / ".env"
        
    @app.get("/api/health")
    async def health(ollama_host: str = DEFAULT_OLLAMA_HOST):
        status_data = await check_ollama_status(ollama_host)
        
        if status_data.get("reachable", False):
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": "ok",
                    "ollama": status_data,
                    "current_model": DEFAULT_OLLAMA_MODEL
                }
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": "error",
                    "message": "Ollama is not reachable",
                    "ollama": status_data,
                    "current_model": DEFAULT_OLLAMA_MODEL
                }
            )
    
    @app.post("/api/model/select")
    async def select_model(req: ModelChangeRequest):
        global DEFAULT_OLLAMA_MODEL
        
        model_name = req.model.strip()
        if not model_name:
            raise HTTPException(status_code=400, detail="Model name is required")
        
        status_data = await check_ollama_status(DEFAULT_OLLAMA_HOST)
        available_models = status_data.get("models", [])
        
        if model_name not in available_models:
            raise HTTPException(
                status_code=404, 
                detail=f"Model '{model_name}' not found. Available: {', '.join(available_models)}"
            )
        
        old_model = DEFAULT_OLLAMA_MODEL
        DEFAULT_OLLAMA_MODEL = model_name
        
        update_env_file(env_path, {'OLLAMA_MODEL': model_name})
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "ok",
                "message": f"Model changed from '{old_model}' to '{model_name}'",
                "current_model": model_name,
                "available_models": available_models
            }
        )
        
    @app.get("/api/model/current")
    async def get_current_model():
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "current_model": DEFAULT_OLLAMA_MODEL
            }
        )
    
    @app.post("/api/telegram/config")
    async def save_telegram_config(req: TelegramConfig):
        env_vars = {
            'TELEGRAM_API_ID': req.api_id,
            'TELEGRAM_API_HASH': req.api_hash,
            'TELEGRAM_PHONE': req.phone
        }
        update_env_file(env_path, env_vars)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "ok",
                "message": "Telegram configuration saved successfully"
            }
        )
        
    @app.get("/api/telegram/config")
    async def get_telegram_config():
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "api_id": get_env_value(env_path, 'TELEGRAM_API_ID'),
                "api_hash": get_env_value(env_path, 'TELEGRAM_API_HASH'),
                "phone": get_env_value(env_path, 'TELEGRAM_PHONE')
            }
        )
        
    @app.post("/api/vk/config")
    async def save_vk_config(req: VkConfig):
        update_env_file(env_path, {'VK_TOKEN': req.token})
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "ok",
                "message": "VK token saved successfully"
            }
        )
        
    @app.get("/api/vk/config")
    async def get_vk_config():
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "token": get_env_value(env_path, 'VK_TOKEN')
            }
        )
    
    @app.get("/api/config/all")
    async def get_all_config():
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "ollama": {
                    "host": DEFAULT_OLLAMA_HOST,
                    "model": DEFAULT_OLLAMA_MODEL
                },
                "telegram": {
                    "api_id": get_env_value(env_path, 'TELEGRAM_API_ID'),
                    "api_hash": get_env_value(env_path, 'TELEGRAM_API_HASH'),
                    "phone": get_env_value(env_path, 'TELEGRAM_PHONE')
                },
                "vk": {
                    "token": get_env_value(env_path, 'VK_TOKEN')
                }
            }
        )
        
    @app.get("/")
    async def serve_index():
        return HTMLResponse(get_status_page())
        
    static_path = WEB_DIR / "static"
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    
    styles_path = WEB_DIR / "styles"
    if styles_path.exists():
        app.mount("/styles", StaticFiles(directory=str(styles_path)), name="styles")
    
    return app