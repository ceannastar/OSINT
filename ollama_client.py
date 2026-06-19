import httpx
from config import DEFAULT_OLLAMA_HOST, DEFAULT_OLLAMA_MODEL


async def check_ollama_status(ollama_host: str = DEFAULT_OLLAMA_HOST) -> dict:
    host = ollama_host.rstrip("/")
    result = {
        "reachable": False,
        "models": [],
        "current_model": DEFAULT_OLLAMA_MODEL,
        "version": None,
        "error": None,
        "host": host,
        "model_details": {}
    }
    
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{host}/api/tags")
            
            if response.status_code == 200:
                result["reachable"] = True
                data = response.json()
                
                models_list = data.get("models", [])
                result["models"] = [m.get("name", "unknown") for m in models_list]
                
                for model in models_list:
                    model_name = model.get("name", "unknown")
                    result["model_details"][model_name] = {
                        "digest": model.get("digest", "")[:12] + "...",
                        "size": model.get("size", 0),
                        "modified_at": model.get("modified_at", ""),
                        "details": model.get("details", {})
                    }
                
                if result["models"]:
                    result["current_model"] = result["models"][0]
                
                try:
                    version_response = await client.get(f"{host}/api/version")
                    if version_response.status_code == 200:
                        version_data = version_response.json()
                        result["version"] = version_data.get("version", "unknown")
                except:
                    pass
                
                current_model = result["current_model"]
                if current_model and current_model in result["model_details"]:
                    details = result["model_details"][current_model]
                    details_info = details.get("details", {})
                    result["model_details"][current_model]["format"] = details_info.get("format", "unknown")
                    result["model_details"][current_model]["family"] = details_info.get("family", "unknown")
                    result["model_details"][current_model]["parameter_size"] = details_info.get("parameter_size", "unknown")
                    result["model_details"][current_model]["quantization_level"] = details_info.get("quantization_level", "unknown")
            else:
                result["error"] = f"HTTP {response.status_code}"
                
    except httpx.ConnectError:
        result["error"] = "Подключение прервано. Ollama запущен?"
    except httpx.TimeoutException:
        result["error"] = "Не удалось подключиться. Время истекло"
    except Exception as e:
        result["error"] = str(e)
    
    return result