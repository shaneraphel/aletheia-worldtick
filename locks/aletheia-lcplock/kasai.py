"""Kasai LCP at an index. Empty text, a bad SA, or a bad index is absence, not 0."""
from __future__ import annotations


def kasai_lcp_at(text: str, sa: list[int], i: int) -> int:
    if not text or not sa or len(sa) != len(text):
        raise ValueError("empty suffix array is absence")
    n = len(text)
    if i <= 0 or i >= n:
        raise ValueError("index is absence")
    rank = [-1] * n
    for p, s in enumerate(sa):
        if s < 0 or s >= n or rank[s] != -1:
            raise ValueError("sa is absence")
        rank[s] = p
    if any(r < 0 for r in rank):
        raise ValueError("sa is absence")
    lcp = [0] * n
    h = 0
    for v in range(n):
        r = rank[v]
        if r == 0:
            continue
        j = sa[r - 1]
        while v + h < n and j + h < n and text[v + h] == text[j + h]:
            h += 1
        lcp[r] = h
        if h:
            h -= 1
    return lcp[i]
