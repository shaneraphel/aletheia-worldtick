"""Cuckoo hashing occupancy. Empty keys or a failed rehash is absence, not 0."""
from __future__ import annotations


def cuckoo_placed(keys: list[int], n: int) -> int:
    if not keys or n <= 0:
        raise ValueError("empty table is absence")
    t1: list[int | None] = [None] * n
    t2: list[int | None] = [None] * n

    def h1(x: int) -> int:
        return x % n

    def h2(x: int) -> int:
        return (2 * x + 1) % n

    max_kick = n * 4
    for key in keys:
        cur = key
        for _ in range(max_kick):
            i = h1(cur)
            if t1[i] is None:
                t1[i] = cur
                break
            t1[i], cur = cur, t1[i]
            j = h2(cur)
            if t2[j] is None:
                t2[j] = cur
                break
            t2[j], cur = cur, t2[j]
        else:
            raise ValueError("rehash is absence")
    return sum(x is not None for x in t1) + sum(x is not None for x in t2)
