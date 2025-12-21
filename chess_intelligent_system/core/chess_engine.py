from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Optional


@dataclass(frozen=True)
class ThinkResult:
    best_uci: str
    candidates_uci: list[str]


def think_best_move(
    fen: str,
    legal_moves_uci: Optional[list[str]] = None,
    *,
    max_candidates: int = 5,
) -> ThinkResult:
    """最小联调实现：随机走子。

    约束：
    - 不解析 fen（仅作为透传字段存在，便于未来接入真正引擎/模型）
    - 必须依赖前端传入 legalMovesUci 才能选棋

    目的：
    - 验证 chess-games-react <-> FastAPI 的协议、跨域与时序没问题

    异常：
    - 未提供 legalMovesUci 或为空时，抛出 ValueError("no-legal-moves")
    """

    _ = fen  # 目前不使用，但保留参数以符合协议

    if not legal_moves_uci:
        raise ValueError("no-legal-moves")

    unique = list(dict.fromkeys(m for m in legal_moves_uci if isinstance(m, str) and m.strip()))
    if not unique:
        raise ValueError("no-legal-moves")

    k = max(1, min(max_candidates, len(unique)))
    candidates = random.sample(unique, k=k)
    best = random.choice(candidates)
    return ThinkResult(best_uci=best, candidates_uci=candidates)
