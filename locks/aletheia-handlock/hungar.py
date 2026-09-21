"""Hungarian min-assignment occupancy. Empty or non-square is absence, not 0."""
from __future__ import annotations


def hungar_cost(cost: list[list[int]]) -> int:
    if not cost:
        raise ValueError("empty hungarian method is absence")
    n = len(cost)
    if any(len(row) != n for row in cost):
        raise ValueError("non-square hungarian is absence")
    used = [False] * n
    best: int | None = None

    def rec(i: int, acc: int) -> None:
        nonlocal best
        if i == n:
            if best is None or acc < best:
                best = acc
            return
        for j in range(n):
            if not used[j]:
                used[j] = True
                rec(i + 1, acc + cost[i][j])
                used[j] = False

    rec(0, 0)
    assert best is not None
    return best
