"""Fewest buses to destination on compiled routes. An uncompiled route list is absence."""
from __future__ import annotations

Z = -1


def num_buses(routes, source, target):
    if routes is None or source is None or target is None:
        raise ValueError("uncompiled routes are absence")
    if source == target:
        return 0
    stop_to_bus = {}
    for i, route in enumerate(routes):
        for stop in route:
            stop_to_bus.setdefault(stop, []).append(i)
    if source not in stop_to_bus or target not in stop_to_bus:
        return -1
    q = [(source, 0)]
    seen_stop = {source}
    seen_bus = set()
    head = 0
    while head < len(q):
        stop, d = q[head]
        head += 1
        for b in stop_to_bus.get(stop, []):
            if b in seen_bus:
                continue
            seen_bus.add(b)
            for nxt in routes[b]:
                if nxt == target:
                    return d + 1
                if nxt not in seen_stop:
                    seen_stop.add(nxt)
                    q.append((nxt, d + 1))
    return -1
