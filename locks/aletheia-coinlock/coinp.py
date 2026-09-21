"""Cheapest compiled coin-path jumps. An uncompiled coin row is absence, not an empty path."""
from __future__ import annotations

Z = -1


def cheapest_jump(coins, max_jump):
    if coins is None or max_jump is None or max_jump < 1 or not coins:
        raise ValueError("uncompiled coin path is absence")
    n = len(coins)
    if coins[0] < 0 or coins[-1] < 0:
        return []
    inf = 10**18
    dp = [inf] * n
    nxt = [-1] * n
    dp[-1] = coins[-1]
    for i in range(n - 2, -1, -1):
        if coins[i] < 0:
            continue
        best = inf
        best_j = -1
        for j in range(i + 1, min(n, i + max_jump + 1)):
            if dp[j] >= inf:
                continue
            cost = coins[i] + dp[j]
            if cost < best or (cost == best and (best_j == -1 or j < best_j)):
                best = cost
                best_j = j
        if best_j != -1:
            dp[i] = best
            nxt[i] = best_j
    if dp[0] >= inf:
        return []
    path = []
    i = 0
    while i != -1:
        path.append(i + 1)
        i = nxt[i]
    return path
