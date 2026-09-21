"""Compiled infection-order count on a line of children.

An empty sick set is absence, not a count of 0.
"""
from __future__ import annotations

Z = -1
MOD = 10**9 + 7


def infection_sequences(n, sick):
    if n is None or n <= 0 or sick is None or not sick:
        raise ValueError("uncompiled infection sequence is absence")
    infected = sorted(set(sick))
    if infected[0] < 0 or infected[-1] >= n:
        raise ValueError("uncompiled infection sequence is absence")
    fact = [1] * (n + 1)
    inv = [1] * (n + 1)
    i = 1
    while i <= n:
        fact[i] = fact[i - 1] * i % MOD
        i += 1
    inv[n] = pow(fact[n], MOD - 2, MOD)
    i = n
    while i > 0:
        inv[i - 1] = inv[i] * i % MOD
        i -= 1
    healthy = n - infected.__len__()
    ans = fact[healthy]
    segs = []
    if infected[0] > 0:
        segs.append((infected[0], False))
    i = 0
    while i + 1 < infected.__len__():
        gap = infected[i + 1] - infected[i] - 1
        if gap > 0:
            segs.append((gap, True))
        i += 1
    if infected[-1] < n - 1:
        segs.append((n - 1 - infected[-1], False))
    for length, mid in segs:
        ans = ans * inv[length] % MOD
        if mid and length > 0:
            ans = ans * pow(2, length - 1, MOD) % MOD
    return ans
