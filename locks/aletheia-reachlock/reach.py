"""Planar two-link inverse kinematics. Unreachable is refusal, not rest-pose zero."""
from __future__ import annotations

import math

def two_link_ik(x: float, y: float, l1: float, l2: float) -> tuple[float, float]:
    if l1 <= 0 or l2 <= 0:
        raise ValueError("link length is absence")
    d2 = x * x + y * y
    reach = (l1 + l2) * (l1 + l2)
    fold = (l1 - l2) * (l1 - l2)
    if d2 > reach or d2 < fold:
        raise ValueError("unreachable")
    cos_e = (d2 - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
    cos_e = max(-1.0, min(1.0, cos_e))
    elbow = math.acos(cos_e)
    shoulder = math.atan2(y, x) - math.atan2(l2 * math.sin(elbow), l1 + l2 * math.cos(elbow))
    return (shoulder, elbow)
