"""SSA φ sites: join blocks with two or more predecessors. Empty CFG is absence."""
from __future__ import annotations


def ssa_phi_count(n: int, preds: list[list[int]]) -> int:
    if n <= 0 or not preds or len(preds) != n:
        raise ValueError("empty cfg is absence")
    n_phi = 0
    for incoming in preds:
        if any(p < 0 or p >= n for p in incoming):
            raise ValueError("pred is absence")
        if len(incoming) >= 2:
            n_phi += 1
    return n_phi
