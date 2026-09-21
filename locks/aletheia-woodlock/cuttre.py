"""Cut off compiled trees in height order. An uncompiled forest is absence, not 0."""
from __future__ import annotations

Z = -1


def cut_off_trees(forest):
    if forest is None or not forest or not forest[0]:
        raise ValueError("uncompiled forest is absence")
    m, n = len(forest), len(forest[0])
    trees = []
    for i in range(m):
        for j in range(n):
            if forest[i][j] > 1:
                trees.append((forest[i][j], i, j))
    trees.sort()

    def bfs(si, sj, ti, tj):
        if si == ti and sj == tj:
            return 0
        seen = {(si, sj)}
        q = [(si, sj, 0)]
        head = 0
        while head < len(q):
            x, y, d = q[head]
            head += 1
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in seen and forest[nx][ny] != 0:
                    if nx == ti and ny == tj:
                        return d + 1
                    seen.add((nx, ny))
                    q.append((nx, ny, d + 1))
        return Z

    steps = 0
    x = y = 0
    for _, i, j in trees:
        d = bfs(x, y, i, j)
        if d == Z:
            return Z
        steps += d
        x, y = i, j
    return steps
