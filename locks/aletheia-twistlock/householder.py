"""Householder reflector. Empty or zero vector is absence, not the identity."""
from __future__ import annotations

def householder_first(x: list[int]) -> int:
    if not x:
        raise ValueError("empty vector is absence")
    n2 = sum(v * v for v in x)
    if n2 == 0:
        raise ValueError("zero vector is absence")
    n = 0
    while n * n < n2:
        n += 1
    if n * n != n2:
        raise ValueError("non-square norm is absence")
    sign = 1 if x[0] >= 0 else -1
    return -sign * n
