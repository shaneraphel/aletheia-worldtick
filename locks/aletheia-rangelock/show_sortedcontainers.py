#!/usr/bin/env python3.12
"""Use SortedList on a lane box. Record empty points. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from rngtree import rngtree_count

PTS = [(0, 0), (1, 1), (3, 3)]


def theirs() -> dict:
    from sortedcontainers import SortedList

    empty = list(SortedList().irange(0, 2))
    filled = SortedList(PTS)
    box = sum(1 for x, y in filled if 0 <= x <= 2 and 0 <= y <= 2)
    return {
        "package": "sortedcontainers",
        "version": __import__("sortedcontainers").__version__,
        "empty_irange": empty,
        "box_count": box,
    }


def ours() -> dict:
    n = rngtree_count(PTS, 0, 2, 0, 2)
    empty = "raised"
    try:
        rngtree_count([], 0, 2, 0, 2)
        empty = "accepted"
    except ValueError:
        pass
    return {"rngtree_count": n, "empty": empty}


def main() -> int:
    rec = {
        "schema": "rangelock.show_sortedcontainers.v1",
        "used": "https://github.com/grantjenks/python-sortedcontainers",
        "built": "three-contact lane box count 2; empty points are absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["rngtree_count"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("rangelock show identity failed")
    if rec["theirs"]["box_count"] != 2:
        raise SystemExit("sortedcontainers box identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
