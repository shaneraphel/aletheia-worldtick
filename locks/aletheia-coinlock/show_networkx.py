#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from coinp import cheapest_jump
COINS=[1,2,4,-1,2]
def theirs():
    import networkx as nx
    G=nx.DiGraph()
    return {"package":"networkx","version":nx.__version__,"empty_nodes":G.number_of_nodes(),"empty_dijkstra":None}
def ours():
    n=cheapest_jump(COINS,2); empty="raised"
    try:
        cheapest_jump([],2); empty="accepted"
    except ValueError:
        pass
    return {"cheapest_jump": n, "empty": empty}
def main():
    rec={"schema":"coinlock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"five coins, jump 2, path 1-3-5; empty coin row is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["cheapest_jump"]!=[1,3,5] or rec["ours"]["empty"]!="raised":
        raise SystemExit("coinlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
