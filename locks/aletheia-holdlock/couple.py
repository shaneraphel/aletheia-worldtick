"""Couples holding hands. An uncompiled row is absence, not swap-count 0."""
from __future__ import annotations

Z = -1


def min_swaps_couples(row):
    if row is None:
        raise ValueError("uncompiled row is absence")
    n = len(row)
    pos = [0] * n
    for i, v in enumerate(row):
        pos[v] = i
    swaps = 0
    for i in range(0, n, 2):
        a = row[i]
        want = a ^ 1
        if row[i + 1] == want:
            continue
        j = pos[want]
        partner = row[i + 1]
        row[i + 1], row[j] = row[j], row[i + 1]
        pos[partner] = j
        pos[want] = i + 1
        swaps += 1
    return swaps
