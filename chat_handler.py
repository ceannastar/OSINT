import json
import time
from typing import AsyncIterator

import httpx
from tool_runner import OLLAMA_TOOLS, run_tool


async def stream_ollama(
    messages: list[dict],
    ollama_host: str,
    ollama_model: str
) -> AsyncIterator[dict]:
    host = ollama_host.rstrip("/")
    msgs = list(messages)
    _MAX_TOOL_ROUNDS = 5
    _tool_rounds = 0
    
    while True:
        _tool_rounds += 1
        if _tool_rounds > _MAX_TOOL_ROUNDS:
            yield {"type": "error", "message": "Tool call limit reached (5 rounds)."}
            return
        
        try:
            payload = {
                "model": ollama_model,
                "messages": msgs,
                "tools": OLLAMA_TOOLS,
                "stream": False,
            }
            
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(f"{host}/api/chat", json=payload)
                
            if response.status_code != 200:
                yield {
                    "type": "error",
                    "message": f"Ollama вернул HTTP {response.status_code}: {response.text[:200]}"
                }
                return
            
            data = response.json()
            
        except httpx.ConnectError:
            yield {
                "type": "error",
                "message": f"Не могу подключиться по адресу {host}. Убедитесь, что Ollama запущен."
            }
            return
        except Exception as exc:
            yield {"type": "error", "message": f"Запрос к Ollama завершился ошибкой: {exc}"}
            return
        
        msg = data.get("message", {})
        content = msg.get("content") or ""
        tool_calls = msg.get("tool_calls") or []
        
        if content:
            yield {"type": "text", "content": content}
        
        if not tool_calls:
            break
        
        tool_results = []
        for tc in tool_calls:
            fn = tc.get("function", {})
            tool_name = fn.get("name", "")
            raw_args = fn.get("arguments", {})
            
            if isinstance(raw_args, str):
                try:
                    raw_args = json.loads(raw_args)
                except Exception:
                    raw_args = {"input": raw_args}
            
            tool_input = raw_args.get("input", "")
            if not tool_input and raw_args:
                tool_input = next(
                    (v for v in raw_args.values() if isinstance(v, str)),
                    str(raw_args)
                )
            
            yield {"type": "tool_start", "tool": tool_name, "input": str(tool_input)}
            
            t0 = time.monotonic()
            result = await run_tool(tool_name, str(tool_input))
            elapsed = round(time.monotonic() - t0, 2)
            
            yield {
                "type": "tool_result",
                "tool": tool_name,
                "output": result,
                "elapsed": elapsed
            }
            
            tool_results.append({
                "role": "tool",
                "content": result
            })
        
        msgs = (
            msgs
            + [{"role": "assistant", "content": content, "tool_calls": tool_calls}]
            + tool_results
        )
    
    yield {"type": "done"}