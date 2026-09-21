"""Compiled max alternating-weight strength of k ordered subarrays.

A missing k-th subarray is absence, not a strength of 0.
"""
from __future__ import annotations

Z = -1


def max_k_subarray_strength(nums, k):
    if nums is None or k is None or k <= 0:
        raise ValueError("uncompiled k-strength is absence")
    n = nums.__len__()
    if n == 0 or k > n:
        raise ValueError("uncompiled k-strength is absence")
    inf = 10**30
    f = [[[-inf, -inf] for _ in range(k + 1)] for _ in range(n + 1)]
    f[0][0][0] = 0
    i = 1
    while i <= n:
        x = nums[i - 1]
        j = 0
        while j <= k:
            sign = 1 if (j & 1) else -1
            val = sign * x * (k - j + 1)
            a = f[i - 1][j][0]
            b = f[i - 1][j][1]
            f[i][j][0] = a if a > b else b
            cur = f[i][j][1]
            ext = b + val
            if ext > cur:
                cur = ext
            if j > 0:
                p0 = f[i - 1][j - 1][0]
                p1 = f[i - 1][j - 1][1]
                prev = p0 if p0 > p1 else p1
                openv = prev + val
                if openv > cur:
                    cur = openv
            f[i][j][1] = cur
            j += 1
        i += 1
    a = f[n][k][0]
    b = f[n][k][1]
    ans = a if a > b else b
    if ans <= -inf // 2:
        return Z
    return ans
