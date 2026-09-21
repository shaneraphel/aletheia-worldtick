"""Givens hypot of a 2-vector. Empty or non-square radius is absence, not 0."""
from __future__ import annotations


def givens_hypot(v: list[int]) -> int:
    if not v or len(v) != 2:
        raise ValueError("empty vector is absence")
    a, b = v
    s = a * a + b * b
    if s == 0:
        raise ValueError("zero vector is absence")
    x = s
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + s // x) // 2
    if x * x != s:
        raise ValueError("non-square radius is absence")
    return x
