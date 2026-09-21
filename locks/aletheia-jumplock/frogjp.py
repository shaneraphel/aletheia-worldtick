"""Frog jump on compiled stones. An uncompiled stone is absence, not False."""
from __future__ import annotations

Z = -1


def can_cross(stones):
    if stones is None:
        raise ValueError("uncompiled stones are absence")
    if not stones or stones[0] != 0:
        raise ValueError("uncompiled stones are absence")
    goal = set(stones)
    last = stones[-1]
    reach = {0: set([0])}
    for s in stones:
        if s not in reach:
            continue
        for k in reach[s]:
            for dk in (k - 1, k, k + 1):
                if dk < 1:
                    continue
                nxt = s + dk
                if nxt == last:
                    return True
                if nxt in goal:
                    if nxt not in reach:
                        reach[nxt] = set()
                    reach[nxt].add(dk)
    return last in reach
