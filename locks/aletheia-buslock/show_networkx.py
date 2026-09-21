#!/usr/bin/env python3.12
"""Use NetworkX on two city routes. Record empty path. Refuse missing table."""
from __future__ import annotations
import json, platform, sys
from busrts import num_buses

def theirs() -> dict:
    import networkx as nx
    empty="raised"
    try:
        nx.shortest_path(nx.Graph(), 1, 6)
        empty="accepted"
    except (nx.NetworkXError, nx.NodeNotFound):
        pass
    g=nx.Graph()
    g.add_edges_from([(1,2),(2,7),(3,6),(6,7)])
    return {"package":"networkx","version":nx.__version__,"empty_path":empty,"n_edges":g.number_of_edges()}

def ours() -> dict:
    n=num_buses([[1,2,7],[3,6,7]],1,6)
    empty="raised"
    try:
        num_buses(None,1,6)
        empty="accepted"
    except ValueError:
        pass
    return {"num_buses":n,"empty":empty}

def main() -> int:
    rec={"schema":"buslock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"two-route city hop 2; missing route table is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["num_buses"]!=2 or rec["ours"]["empty"]!="raised":
        raise SystemExit("buslock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
