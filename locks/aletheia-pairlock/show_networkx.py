#!/usr/bin/env python3.12
"""Use NetworkX matching on a four-finger pairing. Record empty vertices. Refuse here."""
from __future__ import annotations
import json, platform, sys
from blossom import blossom_match

def theirs() -> dict:
    import networkx as nx
    empty = nx.maximal_matching(nx.Graph())
    g = nx.Graph(); g.add_nodes_from(range(4)); g.add_edges_from([(0,1),(2,3)])
    return {"package":"networkx","version":nx.__version__,"empty_matching":sorted(empty),"paired":len(nx.maximal_matching(g))}

def ours() -> dict:
    m = blossom_match(4, [(0,1),(2,3)])
    empty = "raised"
    try:
        blossom_match(0, [])
        empty = "accepted"
    except ValueError:
        pass
    return {"blossom_paired": m, "empty": empty}

def main() -> int:
    rec = {"schema":"pairlock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"four-finger pairing 2; empty n is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["blossom_paired"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("pairlock show identity failed")
    if rec["theirs"]["paired"] != 2:
        raise SystemExit("networkx pairing identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
