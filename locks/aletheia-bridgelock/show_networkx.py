#!/usr/bin/env python3.12
"""Use NetworkX bridges on a lane. Record empty edges. Refuse here."""
from __future__ import annotations
import json, platform, sys
from tarjan import n_bridges

def theirs() -> dict:
    import networkx as nx
    empty=list(nx.bridges(nx.Graph()))
    g=nx.Graph([(0,1),(1,2),(2,0),(2,3)])
    return {"package":"networkx","version":nx.__version__,"empty_bridges":empty,"triangle_pending":len(list(nx.bridges(g)))}

def ours() -> dict:
    n=n_bridges(4,[(0,1),(1,2),(2,0),(2,3)])
    empty="raised"
    try:
        n_bridges(4,[])
        empty="accepted"
    except ValueError:
        pass
    return {"n_bridges": n, "empty": empty}

def main() -> int:
    rec={"schema":"bridgelock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"triangle-plus-pending bridge 1; empty edges are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["n_bridges"]!=1 or rec["ours"]["empty"]!="raised":
        raise SystemExit("bridgelock show identity failed")
    if rec["theirs"]["triangle_pending"]!=1:
        raise SystemExit("networkx bridge identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
