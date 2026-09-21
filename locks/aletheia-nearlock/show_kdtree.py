#!/usr/bin/env python3.12
"""Use stefankoegl/kdtree on a contact tape. Record empty search. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from kdtree import kdtree_near


def theirs() -> dict:
    import sys
    from pathlib import Path

    here = str(Path(__file__).resolve().parent)
    saved = list(sys.path)
    sys.path = [p for p in sys.path if p not in ("", here)]
    sys.modules.pop("kdtree", None)
    try:
        import kdtree as skd

        empty_nn = skd.create(dimensions=2).search_nn((0, 0))
        tree = skd.create([(0, 0), (3, 4)])
        nn = tree.search_nn((3, 4))
        near_x = None
        if nn is not None:
            near_x = nn[0].data[0]
        return {
            "package": "kdtree",
            "version": getattr(skd, "__version__", "?"),
            "empty_search_nn": None if empty_nn is None else str(empty_nn),
            "near_x_on_two_points": near_x,
        }
    finally:
        sys.path = saved
        sys.modules.pop("kdtree", None)


def ours() -> dict:
    x = kdtree_near([(0, 0), (3, 4)], 3, 4)
    empty = "raised"
    try:
        kdtree_near([], 0, 0)
        empty = "accepted"
    except ValueError:
        pass
    return {"kdtree_near_two_points": x, "empty": empty}


def main() -> int:
    rec = {
        "schema": "nearlock.show_kdtree.v1",
        "used": "https://github.com/stefankoegl/kdtree",
        "note": "https://github.com/stefankoegl/kdtree/issues/56",
        "built": "nearest-x on a two-point contact tape; empty points are absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["kdtree_near_two_points"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("nearlock show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
