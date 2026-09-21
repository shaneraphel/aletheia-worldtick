"""Walls that contain compiled virus regions. An uncompiled grid is absence, not 0."""
from __future__ import annotations

Z = -1


def contain_virus(is_infected):
    if is_infected is None or not is_infected:
        raise ValueError("uncompiled virus grid is absence")
    grid = [row[:] for row in is_infected]
    m, n = len(grid), len(grid[0])
    walls = 0

    def regions():
        seen = [[False] * n for _ in range(m)]
        out = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] != 1 or seen[i][j]:
                    continue
                stack = [(i, j)]
                seen[i][j] = True
                cells = []
                threat = set()
                peri = 0
                while stack:
                    x, y = stack.pop()
                    cells.append((x, y))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if not (0 <= nx < m and 0 <= ny < n):
                            continue
                        if grid[nx][ny] == 1 and not seen[nx][ny]:
                            seen[nx][ny] = True
                            stack.append((nx, ny))
                        elif grid[nx][ny] == 0:
                            peri += 1
                            threat.add((nx, ny))
                out.append((cells, threat, peri))
        return out

    while True:
        regs = regions()
        if not regs:
            return walls
        regs.sort(key=lambda r: len(r[1]), reverse=True)
        if not regs[0][1]:
            return walls
        cells, _, peri = regs[0]
        walls += peri
        for x, y in cells:
            grid[x][y] = -1
        for cells, threat, _ in regs[1:]:
            for x, y in threat:
                grid[x][y] = 1
