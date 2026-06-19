from pathlib import Path

ROOT = Path(__file__).parent.parent

WEB_DIR = Path(__file__).parent / "web"

DEFAULT_OLLAMA_MODEL = "llama3.2"
DEFAULT_OLLAMA_HOST = "http://localhost:11434"

CHATS_DIR = Path(__file__).parent / "chats"

GITHUB_URL = "https://github.com/ceannastar/OSINT"

USERNAME_PATTERN = r"@([a-zA-Z0-9_]{3,30})"