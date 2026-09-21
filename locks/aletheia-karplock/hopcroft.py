"""Hopcroft-Karp matching. Empty edges are absence, not matching 0."""
from __future__ import annotations

from collections import deque

def hopcroft_karp(n_left: int, n_right: int, edges: list[tuple[int, int]]) -> int:
    if n_left < 0 or n_right < 0:
        raise ValueError("part sizes are absence")
    if not edges:
        raise ValueError("empty edges are absence")
    adj: list[list[int]] = [[] for _ in range(n_left)]
    for u, v in edges:
        if u < 0 or v < 0 or u >= n_left or v >= n_right:
            raise ValueError("edge is absence")
        adj[u].append(v)
    pair_u = [-1] * n_left
    pair_v = [-1] * n_right
    dist = [0] * n_left

    def bfs() -> bool:
        q: deque[int] = deque()
        for u in range(n_left):
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = -1
        found = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                pu = pair_v[v]
                if pu == -1:
                    found = True
                elif dist[pu] == -1:
                    dist[pu] = dist[u] + 1
                    q.append(pu)
        return found

    def dfs(u: int) -> bool:
        for v in adj[u]:
            pu = pair_v[v]
            if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                pair_u[u] = v
                pair_v[v] = u
                return True
        dist[u] = -1
        return False

    matching = 0
    while bfs():
        for u in range(n_left):
            if pair_u[u] == -1 and dfs(u):
                matching += 1
    return matching
