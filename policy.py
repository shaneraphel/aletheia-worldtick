"""Policy iteration. Empty reward table is absence, not action 0."""
from __future__ import annotations

def policy_iteration(rewards: list[list[int]]) -> int:
    if not rewards or any(not row for row in rewards):
        raise ValueError("empty rewards are absence")
    policy = [0] * len(rewards)
    changed = True
    while changed:
        changed = False
        for s, row in enumerate(rewards):
            best = max(range(len(row)), key=lambda a: row[a])
            if best != policy[s]:
                policy[s] = best
                changed = True
    return policy[0]
