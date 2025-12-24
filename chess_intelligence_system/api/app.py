from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chess_intelligence_system.api.models import (
    AiErrEnvelope,
    AiOkEnvelope,
    AiRequestEnvelope,
    AiServiceError,
    ChessAiThinkRequest,
    ChessAiThinkResponse,
)
from chess_intelligence_system.core.chess_engine import think_best_move


def create_app() -> FastAPI:
    app = FastAPI(title="ChessIntelligenceSystem", version="0.0.1")

    # 允许前端 Vite/React 在开发时跨域访问
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict:
        return {"ok": True}

    @app.post("/v1/chess/think")
    def chess_think(req: AiRequestEnvelope[ChessAiThinkRequest]):
        if req.game != "chess":
            return AiErrEnvelope(error=AiServiceError(message=f"unsupported game: {req.game}", code="400"))

        try:
            result = think_best_move(req.payload.fen, req.payload.legalMovesUci)
        except ValueError as e:
            # 例如 no-legal-moves：请求参数不完整/不合法
            return AiErrEnvelope(error=AiServiceError(message=str(e), code="400"))
        except Exception as e:  # 其他：服务端错误
            return AiErrEnvelope(error=AiServiceError(message=str(e), code="500"))

        resp = ChessAiThinkResponse(
            best={"move": result.best_uci, "confidence": 0.3, "value": 0.0},
            candidates=[{"move": u} for u in result.candidates_uci],
        )
        return AiOkEnvelope(payload=resp)

    return app


app = create_app()
