"""Shortest compiled path eliminating at most k obstacles. Uncompiled grid is absence."""
from __future__ import annotations

Z = -1


def shortest_path_obstacles(grid, k):
    if grid is None or not grid or k is None:
        raise ValueError("uncompiled obstacle path is absence")
    from collections import deque

    rows = len(grid)
    cols = len(grid[0])
    q = deque([(0, 0, k, 0)])
    seen = {(0, 0, k)}
    while q:
        i, j, left, dist = q.popleft()
        if i == rows - 1 and j == cols - 1:
            return dist
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x = i + di
            y = j + dj
            if 0 <= x < rows and 0 <= y < cols:
                nxt = left - grid[x][y]
                if nxt >= 0 and (x, y, nxt) not in seen:
                    seen.add((x, y, nxt))
                    q.append((x, y, nxt, dist + 1))
    return -1
