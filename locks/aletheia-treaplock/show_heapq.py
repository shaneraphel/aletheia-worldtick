#!/usr/bin/env python3.12
"""Use heapq on the same priorities. Record empty pop. Refuse empty tapes."""
from __future__ import annotations
import heapq, json, platform, sys
from treap import treap_root

def theirs() -> dict:
    empty = "raised"
    try:
        heapq.heappop([])
        empty = "accepted"
    except IndexError:
        pass
    h = [(2,5),(4,3),(1,8)]
    heapq.heapify(h)
    return {"package":"stdlib-heapq","empty_pop":empty,"min_prio_key": heapq.nsmallest(1,h)[0][1]}

def ours() -> dict:
    n = treap_root([5, 3, 8], [2, 4, 1])
    empty = "raised"
    try:
        treap_root([], [])
        empty = "accepted"
    except ValueError:
        pass
    return {"treap_root": n, "empty": empty}

def main() -> int:
    rec = {"schema":"treaplock.show_heapq.v1","used":"https://docs.python.org/3/library/heapq.html","built":"treap root 3; empty tapes are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["treap_root"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("treaplock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
