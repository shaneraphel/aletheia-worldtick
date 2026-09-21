"""Shortest path that visits every node. An uncompiled graph is absence, not length 0."""
from __future__ import annotations

Z = -1


def shortest_path_visit(graph):
    if graph is None:
        raise ValueError("uncompiled graph is absence")
    n = len(graph)
    if n < 1:
        raise ValueError("uncompiled graph is absence")
    target = (1 << n) - 1
    q = []
    seen = set()
    i = 0
    while i < n:
        q.append((i, 1 << i, 0))
        seen.add((i, 1 << i))
        i += 1
    head = 0
    while head < len(q):
        u, mask, d = q[head]
        head += 1
        if mask == target:
            return d
        for v in graph[u]:
            nxt = mask | (1 << v)
            key = (v, nxt)
            if key in seen:
                continue
            seen.add(key)
            q.append((v, nxt, d + 1))
    return 0
