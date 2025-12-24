"""开发入口。

运行：
  python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
"""

from chess_intelligence_system.api.app import app

__all__ = ["app"]

