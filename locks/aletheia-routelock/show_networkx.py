#!/usr/bin/env python3.12
"""Use NetworkX Johnson on a lane. Record empty edges. Refuse here."""
from __future__ import annotations
import json, platform, sys
from johnson import johnson_dist

def theirs() -> dict:
    import networkx as nx
    empty = nx.johnson(nx.DiGraph())
    g = nx.DiGraph(); g.add_weighted_edges_from([(0,1,1),(1,2,1)])
    return {"package":"networkx","version":nx.__version__,"empty_johnson":empty,"lane_dist":nx.shortest_path_length(g,0,2,weight="weight")}

def ours() -> dict:
    d = johnson_dist(3, [(0,1,1),(1,2,1)], 0, 2)
    empty = "raised"
    try:
        johnson_dist(3, [], 0, 2)
        empty = "accepted"
    except ValueError:
        pass
    return {"johnson_lane": d, "empty": empty}

def main() -> int:
    rec = {"schema":"routelock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"three-node lane distance 2; empty edges are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["johnson_lane"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("routelock show identity failed")
    if rec["theirs"]["lane_dist"] != 2:
        raise SystemExit("networkx lane identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
