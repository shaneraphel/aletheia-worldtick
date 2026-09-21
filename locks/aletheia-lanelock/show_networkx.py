#!/usr/bin/env python3.12
"""Use NetworkX cycles on a next-pose tape. Record empty next. Refuse here."""
from __future__ import annotations
import json, platform, sys
from floyd import floyd_cycle

def theirs() -> dict:
    import networkx as nx
    empty = list(nx.simple_cycles(nx.DiGraph()))
    tri = nx.DiGraph([(0,1),(1,2),(2,0)])
    return {"package":"networkx","version":nx.__version__,"empty_simple_cycles":empty,"triangle_cycles":len(list(nx.simple_cycles(tri)))}

def ours() -> dict:
    c = floyd_cycle([1,2,0])
    empty = "raised"
    try:
        floyd_cycle([])
        empty = "accepted"
    except ValueError:
        pass
    return {"floyd_cycle": c, "empty": empty}

def main() -> int:
    rec = {"schema":"lanelock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"three-node pose loop 1; empty next is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["floyd_cycle"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("lanelock show identity failed")
    if rec["theirs"]["triangle_cycles"] != 1:
        raise SystemExit("networkx triangle identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
