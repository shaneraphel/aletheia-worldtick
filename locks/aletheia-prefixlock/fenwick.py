"""Fenwick prefix sum. Empty values or a bad index are absence, not 0."""
from __future__ import annotations


def fenwick_prefix(vals: list[int], i: int) -> int:
    if not vals:
        raise ValueError("empty values are absence")
    if i < 0 or i >= len(vals):
        raise ValueError("index is absence")
    bit = [0] * (len(vals) + 1)
    for idx, v in enumerate(vals, start=1):
        j = idx
        while j < len(bit):
            bit[j] += v
            j += j & -j
    acc = 0
    j = i + 1
    while j > 0:
        acc += bit[j]
        j -= j & -j
    return acc
