"""Race car instruction length. An uncompiled target is absence, not moves 0."""
from __future__ import annotations

Z = -1


def race_car(target):
    if target is None:
        raise ValueError("uncompiled target is absence")
    if target < 0:
        raise ValueError("uncompiled target is absence")
    q = [(0, 1, 0)]
    seen = {(0, 1)}
    head = 0
    lim = target * 2 + 3
    while head < len(q):
        pos, speed, d = q[head]
        head += 1
        if pos == target:
            return d
        npos = pos + speed
        nsp = speed * 2
        if (npos, nsp) not in seen and npos > -lim and npos < lim:
            seen.add((npos, nsp))
            q.append((npos, nsp, d + 1))
        nsp = -1 if speed > 0 else 1
        if (pos, nsp) not in seen:
            seen.add((pos, nsp))
            q.append((pos, nsp, d + 1))
    return 0
