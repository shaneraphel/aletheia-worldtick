"""Half-open interval overlap counting with explicit boundary checks."""


def interval_tree_overlap(intervals, point):
    """Count intervals containing ``point`` under [left, right) semantics."""
    if not intervals:
        raise ValueError("empty interval tree is absence")
    if isinstance(point, bool) or not isinstance(point, int):
        raise ValueError("interval-tree point must be an integer")
    if any(
        isinstance(left, bool)
        or isinstance(right, bool)
        or not isinstance(left, int)
        or not isinstance(right, int)
        or left >= right
        for left, right in intervals
    ):
        raise ValueError("invalid interval is absence")
    return sum(left <= point < right for left, right in intervals)
