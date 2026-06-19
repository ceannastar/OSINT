from pathlib import Path

ROOT = Path(__file__).parent.parent

WEB_DIR = Path(__file__).parent / "web"

DEFAULT_OLLAMA_MODEL = "llama3.2"
DEFAULT_OLLAMA_HOST = "http://localhost:11434"

GITHUB_URL = "https://github.com/ceannastar/OSINT"

EMAIL_FIND_RE = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"