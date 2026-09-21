"""Minimum compiled two-finger typing distance. Uncompiled word is absence."""
from __future__ import annotations

Z = -1


def minimum_distance(word):
    if word is None or not word:
        raise ValueError("uncompiled two-finger word is absence")

    def cost(a, b):
        if a < 0:
            return 0
        return abs(a // 6 - b // 6) + abs(a % 6 - b % 6)

    n = len(word)
    codes = [ord(c) - 65 for c in word]
    memo = {}

    def dp(i, f1, f2):
        key = (i, f1, f2)
        if key in memo:
            return memo[key]
        if i == n:
            return 0
        c = codes[i]
        a = cost(f1, c) + dp(i + 1, c, f2)
        b = cost(f2, c) + dp(i + 1, f1, c)
        memo[key] = a if a < b else b
        return memo[key]

    return dp(0, -1, -1)
