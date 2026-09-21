"""Blossom maximum-matching occupancy. Empty vertex set is absence, not 0."""
from __future__ import annotations


def blossom_match(n: int, edges: list[tuple[int, int]]) -> int:
    if n < 1:
        raise ValueError("empty blossom is absence")
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    mate = [-1] * n

    def rec(i: int) -> int:
        if i == n:
            return sum(1 for m in mate if m != -1) // 2
        if mate[i] != -1:
            return rec(i + 1)
        best = rec(i + 1)
        for v in adj[i]:
            if mate[v] == -1:
                mate[i] = v
                mate[v] = i
                got = rec(i + 1)
                if got > best:
                    best = got
                mate[i] = -1
                mate[v] = -1
        return best

    return rec(0)
