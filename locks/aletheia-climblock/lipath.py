"""Longest increasing path on a compiled matrix. Missing matrix is absence, not path 0."""
from __future__ import annotations

Z = -1


def longest_increasing_path(matrix):
    if matrix is None or not matrix or not matrix[0]:
        raise ValueError("uncompiled matrix is absence")
    m = len(matrix)
    n = len(matrix[0])
    memo = {}

    def dfs(i, j):
        key = (i, j)
        if key in memo:
            return memo[key]
        best = 1
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni = i + di
            nj = j + dj
            if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                step = 1 + dfs(ni, nj)
                if step > best:
                    best = step
        memo[key] = best
        return best

    ans = 0
    i = 0
    while i < m:
        j = 0
        while j < n:
            cur = dfs(i, j)
            if cur > ans:
                ans = cur
            j += 1
        i += 1
    return ans
