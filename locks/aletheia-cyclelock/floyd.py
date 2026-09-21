"""Floyd cycle detection. Empty next is absence, not acyclic 0."""
from __future__ import annotations

def floyd_cycle(nxt: list[int]) -> int:
    if not nxt:
        raise ValueError("empty next is absence")
    n = len(nxt)

    def step(i: int) -> int:
        if i < 0 or i >= n:
            return -1
        return nxt[i]

    slow = 0
    fast = 0
    while True:
        slow = step(slow)
        fast = step(step(fast))
        if slow < 0 or fast < 0:
            return 0
        if slow == fast:
            return 1
