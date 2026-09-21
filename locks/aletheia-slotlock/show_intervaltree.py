#!/usr/bin/env python3.12
"""Use chaimleib/intervaltree on world-model slots. Record empty at. Refuse here."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path

def theirs() -> dict:
    here = str(Path(__file__).resolve().parent)
    saved = list(sys.path)
    sys.path = [p for p in sys.path if p not in ("", here)]
    sys.modules.pop("intervaltree", None)
    try:
        from intervaltree import IntervalTree
        empty = list(IntervalTree().at(0))
        tree = IntervalTree()
        tree.addi(0, 4, "a")
        tree.addi(2, 6, "b")
        return {
            "package": "intervaltree",
            "version": __import__("importlib.metadata", fromlist=["version"]).version("intervaltree"),
            "empty_at_0": empty,
            "at_3": len(tree.at(3)),
        }
    finally:
        sys.path = saved
        sys.modules.pop("intervaltree", None)

def ours() -> dict:
    from intervaltree import interval_tree_overlap
    n = interval_tree_overlap([(0, 4), (2, 6)], 3)
    empty = "raised"
    try:
        interval_tree_overlap([], 0)
        empty = "accepted"
    except ValueError:
        pass
    return {"interval_tree_overlap": n, "empty": empty}

def main() -> int:
    rec = {"schema":"slotlock.show_intervaltree.v1","used":"https://github.com/chaimleib/intervaltree","built":"two-slot overlap 2 at time 3; empty intervals are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["interval_tree_overlap"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("slotlock show identity failed")
    if rec["theirs"]["at_3"] != 2:
        raise SystemExit("intervaltree at-3 identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
