"""Tarjan bridge finding. Empty graph is absence, not zero bridges."""
from __future__ import annotations

def n_bridges(n: int, edges: list[tuple[int, int]]) -> int:
    if n < 0:
        raise ValueError("n is absence")
    if not edges:
        raise ValueError("empty graph is absence")
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        if u < 0 or v < 0 or u >= n or v >= n or u == v:
            raise ValueError("edge is absence")
        adj[u].append(v)
        adj[v].append(u)
    tin = [-1] * n
    low = [-1] * n
    timer = 0
    bridges = 0

    def dfs(u: int, p: int) -> None:
        nonlocal timer, bridges
        tin[u] = low[u] = timer
        timer += 1
        for v in adj[u]:
            if v == p:
                continue
            if tin[v] != -1:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    bridges += 1

    for i in range(n):
        if tin[i] == -1:
            dfs(i, -1)
    return bridges
