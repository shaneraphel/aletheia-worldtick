"""Kahn layer assignment. Negative n is absence, not zero layers."""
from __future__ import annotations

def kahn_layers(n: int, edges: list[tuple[int, int]]) -> int:
    if n < 0:
        raise ValueError("n is absence")
    indeg = [0] * n
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        if u < 0 or v < 0 or u >= n or v >= n:
            raise ValueError("edge is absence")
        adj[u].append(v)
        indeg[v] += 1
    layer = [i for i in range(n) if indeg[i] == 0]
    n_layers = 0
    seen = 0
    while layer:
        n_layers += 1
        seen += len(layer)
        nxt: list[int] = []
        for u in layer:
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    nxt.append(v)
        layer = nxt
    if seen != n:
        return 0
    return n_layers
