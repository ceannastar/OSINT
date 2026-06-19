from pathlib import Path
from config import WEB_DIR


def get_status_page() -> str:
    index_path = WEB_DIR / "index.html"
    
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    
    return """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BFElite</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0a0f;
            color: #e8e8f0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            width: 100%;
            background: rgba(26, 26, 46, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(100, 100, 255, 0.15);
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }
        h1 { text-align: center; }
        .logo-title {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #00ffc8, #7c3aed, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }
        p { color: #6a6a80; text-align: center; }
        code { background: rgba(255,255,255,0.05); padding: 2px 10px; border-radius: 4px; color: #00ffc8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo-title">BFElite</div>
        <p>Страница статуса не найдена. Проверьте web/index.html</p>
        <p>POST <code>/api/chat</code> с {"message": "Hello!"}</p>
    </div>
</body>
</html>"""