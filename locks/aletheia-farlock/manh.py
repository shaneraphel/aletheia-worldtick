"""Compiled min max-Manhattan after deleting one point.

An empty point set is absence, not a distance of 0.
"""
from __future__ import annotations

Z = -1


def _span(pts):
    if not pts:
        return 0
    smax = smin = pts[0][0] + pts[0][1]
    dmax = dmin = pts[0][0] - pts[0][1]
    i = 1
    while i < pts.__len__():
        s = pts[i][0] + pts[i][1]
        d = pts[i][0] - pts[i][1]
        if s > smax:
            smax = s
        if s < smin:
            smin = s
        if d > dmax:
            dmax = d
        if d < dmin:
            dmin = d
        i += 1
    a = smax - smin
    b = dmax - dmin
    return a if a > b else b


def min_manhattan_after_remove(points):
    if points is None:
        raise ValueError("uncompiled manhattan is absence")
    n = points.__len__()
    if n == 0:
        raise ValueError("uncompiled manhattan is absence")
    if n <= 2:
        return 0
    smax = smin = dmax = dmin = 0
    si_max = si_min = di_max = di_min = 0
    i = 0
    while i < n:
        s = points[i][0] + points[i][1]
        d = points[i][0] - points[i][1]
        if i == 0 or s > smax:
            smax = s
            si_max = i
        if i == 0 or s < smin:
            smin = s
            si_min = i
        if i == 0 or d > dmax:
            dmax = d
            di_max = i
        if i == 0 or d < dmin:
            dmin = d
            di_min = i
        i += 1
    ans = smax - smin
    bd = dmax - dmin
    if bd > ans:
        ans = bd
    for drop in (si_max, si_min, di_max, di_min):
        kept = []
        i = 0
        while i < n:
            if i != drop:
                kept.append(points[i])
            i += 1
        cur = _span(kept)
        if cur < ans:
            ans = cur
    return ans
