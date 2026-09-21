"""Dinic blocking flow. Empty graph is absence, not flow 0."""
from __future__ import annotations

from collections import deque

def dinic_max_flow(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    if n < 2 or s < 0 or t < 0 or s >= n or t >= n or s == t:
        raise ValueError("terminals are absence")
    if not edges:
        raise ValueError("empty graph is absence")
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    caps: list[int] = []

    def add(u: int, v: int, c: int) -> None:
        graph[u].append((v, len(caps)))
        caps.append(c)
        graph[v].append((u, len(caps)))
        caps.append(0)

    for u, v, c in edges:
        if c < 0 or u < 0 or v < 0 or u >= n or v >= n:
            raise ValueError("edge is absence")
        add(u, v, c)

    def bfs(level: list[int]) -> bool:
        q = deque([s])
        level[s] = 0
        while q:
            u = q.popleft()
            for v, i in graph[u]:
                if caps[i] > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    q.append(v)
        return level[t] >= 0

    def dfs(u: int, pushed: int, level: list[int], it: list[int]) -> int:
        if u == t or pushed == 0:
            return pushed
        while it[u] < len(graph[u]):
            v, i = graph[u][it[u]]
            if caps[i] > 0 and level[v] == level[u] + 1:
                tr = dfs(v, min(pushed, caps[i]), level, it)
                if tr:
                    caps[i] -= tr
                    caps[i ^ 1] += tr
                    return tr
            it[u] += 1
        return 0

    flow = 0
    while True:
        level = [-1] * n
        if not bfs(level):
            break
        it = [0] * n
        while True:
            pushed = dfs(s, 10**9, level, it)
            if not pushed:
                break
            flow += pushed
    return flow
