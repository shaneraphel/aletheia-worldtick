"""Bloom filter maybe-membership. Empty keys or a non-positive width are absence."""
from __future__ import annotations


def bloom_maybe(keys: list[int], m: int, k: int, q: int) -> int:
    if not keys or m <= 0 or k <= 0:
        raise ValueError("empty filter is absence")
    bits = [0] * m

    def hashes(x: int) -> list[int]:
        return [((x * (i + 1) * 1103515245 + 12345) % m) for i in range(k)]

    for x in keys:
        for h in hashes(x):
            bits[h] = 1
    return 1 if all(bits[h] for h in hashes(q)) else 0
