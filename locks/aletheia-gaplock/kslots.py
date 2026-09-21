"""Day when two compiled blooms have k empty slots between them. Uncompiled bulbs are absence, not day 0."""
from __future__ import annotations

Z = -1


def k_empty_slots(bulbs, k):
    if bulbs is None or k is None or k < 0 or not bulbs:
        raise ValueError("uncompiled empty slots are absence")
    n = len(bulbs)
    days = [0] * n
    for d, pos in enumerate(bulbs, 1):
        days[pos - 1] = d
    ans = Z
    left = 0
    right = k + 1
    while right < n:
        jumped = False
        for i in range(left + 1, right):
            if days[i] < days[left] or days[i] < days[right]:
                left = i
                right = i + k + 1
                jumped = True
                break
        if jumped:
            continue
        day = days[left] if days[left] > days[right] else days[right]
        if ans == Z or day < ans:
            ans = day
        left = right
        right = left + k + 1
    return ans
