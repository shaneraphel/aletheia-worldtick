#!/usr/bin/env python3.12
"""Use NetworkX components on lane ids. Record empty graph. Refuse negative n."""
from __future__ import annotations
import json, platform, sys
from orbits import DisjointSet

def theirs() -> dict:
    import networkx as nx
    empty = nx.number_connected_components(nx.Graph())
    g = nx.Graph(); g.add_nodes_from(range(4)); g.add_edges_from([(0,1),(2,3)])
    return {"package":"networkx","version":nx.__version__,"empty_components":empty,"paired_components":nx.number_connected_components(g)}

def ours() -> dict:
    d = DisjointSet(4); d.union(0,1); d.union(2,3)
    empty = "raised"
    try:
        DisjointSet(-1)
        empty = "accepted"
    except ValueError:
        pass
    return {"n_orbits": d.n_orbits(), "negative_n": empty}

def main() -> int:
    rec={"schema":"orbitlock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"four-node lane orbits 2; negative n is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["n_orbits"]!=2 or rec["ours"]["negative_n"]!="raised":
        raise SystemExit("orbitlock show identity failed")
    if rec["theirs"]["paired_components"]!=2:
        raise SystemExit("networkx component identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
