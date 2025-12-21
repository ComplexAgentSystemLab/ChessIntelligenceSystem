import pytest
import httpx

from chess_intelligent_system.api.app import create_app


@pytest.mark.anyio
async def test_chess_think_ok():
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/chess/think",
            json={
                "game": "chess",
                "payload": {
                    "fen": "any-fen-is-ok-in-smoke-test",
                    "legalMovesUci": ["e2e4", "g1f3", "d2d4"],
                },
            },
        )

    data = res.json()
    assert data["ok"] is True
    best = data["payload"]["best"]["move"]
    moves = [c["move"] for c in data["payload"].get("candidates", [])]
    assert best in moves


@pytest.mark.anyio
async def test_chess_think_missing_legal_moves_returns_error_envelope():
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/chess/think",
            json={
                "game": "chess",
                "payload": {"fen": "any"},
            },
        )

    data = res.json()
    assert data["ok"] is False
    assert "no-legal-moves" in data["error"]["message"]


@pytest.mark.anyio
async def test_chess_think_unsupported_game():
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/chess/think",
            json={
                "game": "go",
                "payload": {
                    "fen": "any",
                    "legalMovesUci": ["irrelevant"],
                },
            },
        )

    data = res.json()
    assert data["ok"] is False
    assert data["error"]["code"] == "400"
