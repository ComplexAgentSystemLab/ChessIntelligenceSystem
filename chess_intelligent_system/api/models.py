from __future__ import annotations

from typing import Generic, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field


AiGameId = Literal["chess", "go", "chinese-chess"]


class AiServiceError(BaseModel):
    message: str
    code: Optional[str] = None
    detail: Optional[object] = None


TPayload = TypeVar("TPayload")


class AiRequestEnvelope(BaseModel, Generic[TPayload]):
    game: AiGameId
    model: Optional[str] = None
    payload: TPayload


class AiOkEnvelope(BaseModel, Generic[TPayload]):
    ok: Literal[True] = True
    payload: TPayload


class AiErrEnvelope(BaseModel):
    ok: Literal[False] = False
    error: AiServiceError


AiResponseEnvelope = Union[AiOkEnvelope[TPayload], AiErrEnvelope]


class ChessAiThinkRequest(BaseModel):
    fen: str = Field(..., description="FEN 局面")
    legalMovesUci: Optional[list[str]] = Field(default=None, description="可选：合法走法 UCI 列表")


class AiMoveSuggestion(BaseModel):
    move: str
    confidence: Optional[float] = None
    value: Optional[float] = None
    comment: Optional[str] = None


class ChessAiThinkResponse(BaseModel):
    best: AiMoveSuggestion
    candidates: Optional[list[AiMoveSuggestion]] = None

