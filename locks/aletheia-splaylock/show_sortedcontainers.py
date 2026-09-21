#!/usr/bin/env python3.12
"""Use SortedSet on three keys. Record empty membership. Refuse empty tree."""
from __future__ import annotations
import json, platform, sys
from splay import splay_root

def theirs() -> dict:
    from sortedcontainers import SortedSet
    empty = 1 in SortedSet()
    s = SortedSet([2, 1, 3])
    return {"package":"sortedcontainers","version":__import__("sortedcontainers").__version__,"empty_membership":empty,"has_1": 1 in s}

def ours() -> dict:
    n = splay_root([2, 1, 3], 1)
    empty = "raised"
    try:
        splay_root([], 1)
        empty = "accepted"
    except ValueError:
        pass
    return {"splay_root": n, "empty": empty}

def main() -> int:
    rec = {"schema":"splaylock.show_sortedcontainers.v1","used":"https://github.com/grantjenks/python-sortedcontainers","built":"splay-to-root 1 on [2,1,3]; empty tree is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["splay_root"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("splaylock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
