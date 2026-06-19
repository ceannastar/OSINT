import asyncio
import subprocess
import re
from typing import Optional
import httpx
from bs4 import BeautifulSoup


TOOL_CATALOG: list[dict] = [
    {
        "name": "search_username",
        "description": "Просмотреть платформы, в которых может присутствовать данный username",
        "input_label": "Username",
        "input_placeholder": "johndoe99",
    },
    {
        "name": "scrape_website",
        "description": "Извлечь максимальное содержимое из сайта при помощи BeautifulSoup.",
        "input_label": "Website URL",
        "input_placeholder": "https://example.com",
    },
]

OLLAMA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": f"{tool['input_label']} — e.g. {tool['input_placeholder']}",
                    }
                },
                "required": ["input"],
            },
        },
    }
    for tool in TOOL_CATALOG
]


async def run_tool(tool_name: str, tool_input: str) -> str:
    if tool_name == "search_username":
        return await run_sherlock(tool_input)
    elif tool_name == "scrape_website":
        return await scrape_website(tool_input)
    else:
        return f"Info: Tool {tool_name} not implemented"


async def run_sherlock(username: str) -> str:
    import os
    
    try:
        result = subprocess.run(
            ["sherlock", "--help"],
            capture_output=True,
            timeout=5
        )
        if result.returncode != 0:
            return "Ошибка: Sherlock не установлен. Переустановите зависимости"
        
        output_file = f"{username}.txt"
        
        if os.path.exists(output_file):
            os.remove(output_file)
        
        process = await asyncio.create_subprocess_exec(
            "sherlock", username,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        stdout_output = stdout.decode('utf-8', errors='ignore')
        stderr_output = stderr.decode('utf-8', errors='ignore')
        
        if process.returncode != 0 and process.returncode != 1:
            if "No results" not in stderr_output:
                return f"Error: sherlock execution failed: {stderr_output[:200]}"
        
        content = ""
        
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                os.remove(output_file)
            except:
                pass
        else:
            content = stdout_output
        
        lines = content.split('\n')
        urls = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            url_match = re.search(r'https?://[^\s]+', line)
            if url_match:
                urls.append(url_match.group(0))
        
        if urls:
            result_text = f"Найдено профилей '{username}':\n\n"
            result_text += '\n'.join(urls)
            result_text += f"\n\nВсего нашлось: {len(urls)} платформ"
            return result_text
        else:
            return f"Пользователь '{username}' не был найден"
        
    except FileNotFoundError:
        return "Ошибка: Sherlock не найден. Переустановите зависимости"
    except Exception as e:
        return f"Ошибка: sherlock не смог запуститься: {str(e)}"


async def scrape_website(url: str) -> str:
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            response = await client.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code != 200:
                return f"Ошибка: Не могу загрузить страницу (HTTP {response.status_code})"
            
            html_content = response.text
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.decompose()
        
        result_parts = []
        
        title = soup.find('title')
        if title:
            result_parts.append(f"Title: {title.get_text().strip()}")
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            result_parts.append(f"Description: {meta_desc.get('content').strip()}")
        
        content_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article', 'section', 'main'])
        
        content_text = []
        for tag in content_tags:
            text = tag.get_text().strip()
            if text and len(text) > 20:  
                content_text.append(text)
        
        full_content = '\n'.join(content_text)
        if len(full_content) > 4000:
            full_content = full_content[:4000] + "\n... (обрезано содержимого)"
        
        if full_content:
            result_parts.append(f"\nContent:\n{full_content}")
        
        links = soup.find_all('a', href=True)
        unique_links = []
        for link in links:
            href = link.get('href')
            if href and href.startswith(('http://', 'https://')) and href not in unique_links:
                unique_links.append(href)
                if len(unique_links) >= 100:  
                    break
        
        if unique_links:
            result_parts.append(f"\nLinks ({len(unique_links)}):")
            for link in unique_links[:15]:
                result_parts.append(f"  - {link}")
            if len(unique_links) > 15:
                result_parts.append(f"  ... and {len(unique_links) - 15} more")
        
        if not result_parts:
            return "Ошибка: нет контента"
        
        return '\n'.join(result_parts)
        
    except httpx.TimeoutException:
        return "Ошибка: Превышено время - страница большая, чтобы её просмотреть"
    except httpx.ConnectError:
        return "Ошибка: Не могу подключиться к веб-сайту"
    except Exception as e:
        return f"Ошибка: Ошибка при парсинге сайта: {str(e)}"


def detect_target(message: str) -> tuple[Optional[str], Optional[str]]:
    from config import USERNAME_PATTERN
    
    username_pattern = re.compile(USERNAME_PATTERN)
    username_match = username_pattern.search(message)
    
    url_match = re.search(r'https?://[^\s]+', message)
    
    if username_match:
        return ("username", username_match.group(1))
    elif url_match:
        return ("url", url_match.group(0))
    else:
        return (None, None)