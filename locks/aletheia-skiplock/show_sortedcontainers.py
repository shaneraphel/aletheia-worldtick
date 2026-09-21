#!/usr/bin/env python3.12
"""Use SortedList on a sorted tape. Record empty index. Refuse empty list."""
from __future__ import annotations
import json, platform, sys
from skiplist import skip_search

def theirs() -> dict:
    from sortedcontainers import SortedList
    empty = "raised"
    try:
        SortedList().index(5)
        empty = "accepted"
    except ValueError:
        pass
    return {"package":"sortedcontainers","version":__import__("sortedcontainers").__version__,"empty_index":empty,"index_5": SortedList([1,3,5,7]).index(5)}

def ours() -> dict:
    n = skip_search([1, 3, 5, 7], 5)
    empty = "raised"
    try:
        skip_search([], 5)
        empty = "accepted"
    except ValueError:
        pass
    return {"skip_search": n, "empty": empty}

def main() -> int:
    rec = {"schema":"skiplock.show_sortedcontainers.v1","used":"https://github.com/grantjenks/python-sortedcontainers","built":"skip index 2 for key 5; empty list is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["skip_search"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("skiplock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
