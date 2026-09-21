"""Compiled non-overlapping job-profit schedule. Uncompiled jobs are absence, not 0."""
from __future__ import annotations

Z = -1


def job_scheduling(start_time, end_time, profit):
    if start_time is None or end_time is None or profit is None or not start_time:
        raise ValueError("uncompiled job schedule is absence")
    import bisect

    jobs = sorted(zip(start_time, end_time, profit), key=lambda x: x[1])
    ends = [j[1] for j in jobs]
    dp = [0] * len(jobs)
    for i, (s, _e, p) in enumerate(jobs):
        j = bisect.bisect_right(ends, s, 0, i) - 1
        take = p + (dp[j] if j >= 0 else 0)
        skip = dp[i - 1] if i else 0
        dp[i] = take if take > skip else skip
    return dp[-1]
