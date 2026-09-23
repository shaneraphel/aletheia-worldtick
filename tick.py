"""One discrete world tick. Empty facts are absence, not zero reachable.

`world_tick` moves each occupied fact across one outgoing edge.
`datalog_fixpoint` is the later closure. On a path of length 2 they disagree.
"""
from __future__ import annotations


def _mark(n: int, facts: list[int]) -> list[bool]:
    if n < 0:
        raise ValueError("n is absence")
    if not facts:
        raise ValueError("empty facts are absence")
    reach = [False] * n
    for f in facts:
        if f < 0 or f >= n:
            raise ValueError("fact is absence")
        reach[f] = True
    return reach


def _step(n: int, reach: list[bool], edges: list[tuple[int, int]]) -> list[bool]:
    nxt = reach[:]
    for u, v in edges:
        if u < 0 or v < 0 or u >= n or v >= n:
            raise ValueError("edge is absence")
        if reach[u]:
            nxt[v] = True
    return nxt


def world_tick(n: int, facts: list[int], edges: list[tuple[int, int]]) -> int:
    reach = _mark(n, facts)
    nxt = _step(n, reach, edges)
    return sum(1 for x in nxt if x)


def reach_after(n: int, facts: list[int], edges: list[tuple[int, int]], horizon: int) -> int:
    if horizon < 0:
        raise ValueError("horizon is absence")
    reach = _mark(n, facts)
    for _ in range(horizon):
        nxt = _step(n, reach, edges)
        if nxt == reach:
            break
        reach = nxt
    return sum(1 for x in reach if x)
