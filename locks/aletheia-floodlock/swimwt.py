"""Swim in rising water on a compiled elevation grid. An uncompiled grid is absence."""
from __future__ import annotations

Z = -1


def swim_rising(grid):
    if grid is None or not grid:
        raise ValueError("uncompiled grid is absence")
    n = len(grid)
    lo = grid[0][0]
    hi = max(max(row) for row in grid)

    def ok(t):
        if grid[0][0] > t:
            return False
        seen = {(0, 0)}
        stack = [(0, 0)]
        while stack:
            r, c = stack.pop()
            if r == n - 1 and c == n - 1:
                return True
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen and grid[nr][nc] <= t:
                    seen.add((nr, nc))
                    stack.append((nr, nc))
        return False

    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
