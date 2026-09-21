"""Two-modulus CRT. Non-coprime or non-positive moduli are absence, not 0."""
from __future__ import annotations


def crt_pair(a: int, m: int, b: int, n: int) -> int:
    if m <= 0 or n <= 0:
        raise ValueError("modulus is absence")

    def egcd(x: int, y: int) -> tuple[int, int, int]:
        if y == 0:
            return x, 1, 0
        g, s, t = egcd(y, x % y)
        return g, t, s - (x // y) * t

    g, inv, _ = egcd(m, n)
    if g != 1:
        raise ValueError("non-coprime moduli are absence")
    return (a + m * ((b - a) * inv % n)) % (m * n)
