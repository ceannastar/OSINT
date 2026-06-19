import uvicorn
from app import create_app


def run_server(host: str = "0.0.0.0", port: int = 8080) -> None:
    app = create_app()
    print(f"[*] BFElite OSINT Platform web server")
    print(f"[*] Server → http://{host}:{port}/")
    print(f"[*] POST /api/chat → AI chat endpoint")
    print(f"[*] GET /api/health → Ollama status check")
    print("[*] Press Ctrl+C to stop.")
    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    run_server()