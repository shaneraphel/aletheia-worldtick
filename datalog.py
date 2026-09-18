"""Datalog fixpoint. Empty facts are absence, not zero reachable."""
from __future__ import annotations

def datalog_fixpoint(n: int, facts: list[int], edges: list[tuple[int, int]]) -> int:
    if n < 0:
        raise ValueError("n is absence")
    if not facts:
        raise ValueError("empty facts are absence")
    reach = [False] * n
    for f in facts:
        if f < 0 or f >= n:
            raise ValueError("fact is absence")
        reach[f] = True
    changed = True
    while changed:
        changed = False
        for u, v in edges:
            if u < 0 or v < 0 or u >= n or v >= n:
                raise ValueError("edge is absence")
            if reach[u] and not reach[v]:
                reach[v] = True
                changed = True
    return sum(1 for x in reach if x)
