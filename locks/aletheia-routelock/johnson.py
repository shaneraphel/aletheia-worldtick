"""Johnson shortest-path occupancy. Empty, unreachable, or a negative cycle is absence, not 0."""
from __future__ import annotations


def johnson_dist(
    n: int, edges: list[tuple[int, int, int]], src: int, dst: int
) -> int:
    if n < 1 or not edges:
        raise ValueError("empty johnson is absence")
    if src < 0 or dst < 0 or src >= n or dst >= n:
        raise ValueError("johnson vertex out of range is absence")
    dist: list[int | None] = [None] * n
    dist[src] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] is not None:
                cand = dist[u] + w
                if dist[v] is None or cand < dist[v]:
                    dist[v] = cand
    for u, v, w in edges:
        if dist[u] is not None and (dist[v] is None or dist[u] + w < dist[v]):
            raise ValueError("johnson negative cycle is absence")
    if dist[dst] is None:
        raise ValueError("johnson unreachable is absence")
    return dist[dst]
