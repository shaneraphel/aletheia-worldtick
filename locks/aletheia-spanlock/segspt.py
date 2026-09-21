"""Segment-tree range sum. Empty array or a bad range is absence, not 0."""
from __future__ import annotations


def segspt_sum(a: list[int], left: int, right: int) -> int:
    if not a:
        raise ValueError("empty array is absence")
    if left < 0 or right < left or right >= len(a):
        raise ValueError("range is absence")
    n = len(a)
    t = [0] * (4 * n)

    def build(v: int, tl: int, tr: int) -> None:
        if tl == tr:
            t[v] = a[tl]
            return
        tm = (tl + tr) // 2
        build(v * 2, tl, tm)
        build(v * 2 + 1, tm + 1, tr)
        t[v] = t[v * 2] + t[v * 2 + 1]

    def query(v: int, tl: int, tr: int, l: int, r: int) -> int:
        if l > r:
            return 0
        if l == tl and r == tr:
            return t[v]
        tm = (tl + tr) // 2
        return query(v * 2, tl, tm, l, min(r, tm)) + query(
            v * 2 + 1, tm + 1, tr, max(l, tm + 1), r
        )

    build(1, 0, n - 1)
    return query(1, 0, n - 1, left, right)
