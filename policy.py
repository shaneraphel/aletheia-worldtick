"""Integer policy iteration. An empty reward table is absence, not action 0.

Transition is the ring `(state + action + 1) % n_states`.
Continuation is `reward + (9 * V[next]) // 10`.
The returned action is the policy at state 0.
Row-0 greedy reads only the current row, so the two actions can differ.
"""
from __future__ import annotations


def _check(reward: list[list[int]]) -> tuple[int, int]:
    if not reward or not reward[0]:
        raise ValueError("empty reward table is absence")
    n = len(reward)
    a = len(reward[0])
    if any(len(row) != a or not row for row in reward):
        raise ValueError("empty reward table is absence")
    return n, a


def _nxt(n: int, state: int, action: int) -> int:
    return (state + action + 1) % n


def row0_greedy(reward: list[list[int]]) -> int:
    _check(reward)
    row = reward[0]
    best_a = 0
    best = row[0]
    for i, v in enumerate(row):
        if v > best:
            best = v
            best_a = i
    return best_a


def policy_iteration(reward: list[list[int]]) -> int:
    n, a = _check(reward)
    policy = [0] * n
    values = [0] * n
    for _epoch in range(n + 1):
        for _sweep in range(64):
            nv = [0] * n
            for s in range(n):
                act = policy[s]
                nv[s] = reward[s][act] + (9 * values[_nxt(n, s, act)]) // 10
            if nv == values:
                break
            values = nv
        improved = False
        for s in range(n):
            best_a = 0
            best_q = reward[s][0] + (9 * values[_nxt(n, s, 0)]) // 10
            for act in range(1, a):
                q = reward[s][act] + (9 * values[_nxt(n, s, act)]) // 10
                if q > best_q:
                    best_q = q
                    best_a = act
            if best_a != policy[s]:
                policy[s] = best_a
                improved = True
        if not improved:
            break
    return policy[0]
