#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from frogjp import can_cross
STONES=[0,1,3,5,6,8,12,17]
def theirs():
    import networkx as nx
    G=nx.Graph()
    return {"package":"networkx","version":nx.__version__,"empty_nodes":G.number_of_nodes(),"empty_components":nx.number_connected_components(G)}
def ours():
    n=can_cross(STONES); empty="raised"
    try:
        can_cross([]); empty="accepted"
    except ValueError:
        pass
    return {"can_cross": n, "empty": empty}
def main():
    rec={"schema":"jumplock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"eight compiled stones cross; empty stones are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["can_cross"] is not True or rec["ours"]["empty"]!="raised":
        raise SystemExit("jumplock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
