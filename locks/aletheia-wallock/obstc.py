"""Compiled minimum obstacle removals on a 0-1 grid walk.

Planted 2026-09-19: leftover19 dests after LC2035 stayed occupancy-only
because the intern bank had no unique body. An empty cell costs 0 and
an obstacle costs 1. Uncompiled grid is absence, not a removal count
of 0.
"""
from __future__ import annotations

from collections import deque

Z = -1


def min_obstacle_removal(grid):
    if grid is None or not grid or not grid[0]:
        raise ValueError("uncompiled obstacle grid is absence")
    h = grid.__len__()
    w = grid[0].__len__()
    inf = 10**18
    dist = [[inf] * w for _ in range(h)]
    dist[0][0] = grid[0][0]
    q = deque([(0, 0)])
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while q:
        r, c = q.popleft()
        d = dist[r][c]
        k = 0
        while k < 4:
            nr = r + dirs[k][0]
            nc = c + dirs[k][1]
            k += 1
            if nr < 0 or nr >= h or nc < 0 or nc >= w:
                continue
            nd = d + grid[nr][nc]
            if nd < dist[nr][nc]:
                dist[nr][nc] = nd
                if grid[nr][nc] == 0:
                    q.appendleft((nr, nc))
                else:
                    q.append((nr, nc))
    if dist[h - 1][w - 1] >= inf:
        raise ValueError("uncompiled obstacle grid is absence")
    return dist[h - 1][w - 1]
