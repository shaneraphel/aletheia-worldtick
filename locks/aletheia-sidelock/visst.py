"""Compiled visible-from-left stick arrangements. Uncompiled n is absence."""
from __future__ import annotations

Z = -1


def ways_rearrange_sticks(n, k):
    if n is None or k is None or n < 1 or k < 1:
        raise ValueError("uncompiled stick arrangements are absence")
    mod = 10**9 + 7
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    i = 1
    while i <= n:
        j = 1
        while j <= k and j <= i:
            dp[i][j] = (dp[i - 1][j - 1] + (i - 1) * dp[i - 1][j]) % mod
            j += 1
        i += 1
    return dp[n][k]
