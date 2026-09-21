#!/usr/bin/env python3.12
"""Use NetworkX on a one-node tree. Record empty graph. Refuse missing tree."""
from __future__ import annotations
import json, platform, sys
from camtree import min_camera_cover

def theirs() -> dict:
    import networkx as nx
    empty = list(nx.Graph().nodes())
    g = nx.Graph(); g.add_node(0)
    return {"package":"networkx","version":nx.__version__,"empty_nodes":empty,"n_nodes": g.number_of_nodes()}

def ours() -> dict:
    n = min_camera_cover([0])
    empty = "raised"
    try:
        min_camera_cover(None)
        empty = "accepted"
    except ValueError:
        pass
    return {"min_camera_cover": n, "empty": empty}

def main() -> int:
    rec={"schema":"camlock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"one-node camera cover 1; missing tree is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["min_camera_cover"]!=1 or rec["ours"]["empty"]!="raised":
        raise SystemExit("camlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
