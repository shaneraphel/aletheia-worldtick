"""Minimum compiled taps that water the whole garden. Uncompiled ranges are absence."""
from __future__ import annotations

Z = -1


def min_taps(n, ranges):
    if n is None or ranges is None or n < 1:
        raise ValueError("uncompiled garden taps are absence")
    reach = [0] * (n + 1)
    for i, r in enumerate(ranges):
        left = 0 if i - r < 0 else i - r
        right = n if i + r > n else i + r
        if right > reach[left]:
            reach[left] = right
    ans = 0
    cur = 0
    nxt = 0
    for i in range(n):
        if i > nxt:
            return -1
        if reach[i] > nxt:
            nxt = reach[i]
        if i == cur:
            ans += 1
            cur = nxt
    return ans if cur >= n else -1
