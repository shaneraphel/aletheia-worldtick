#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from visitall import shortest_path_visit
G=[[1,2,3],[0],[0],[0]]
def theirs():
    import networkx as nx
    empty=list(nx.Graph().nodes())
    g=nx.Graph([(0,1),(0,2),(0,3)])
    return {"package":"networkx","version":nx.__version__,"empty_nodes":empty,"n_nodes":g.number_of_nodes()}
def ours():
    n=shortest_path_visit(G); empty="raised"
    try:
        shortest_path_visit([]); empty="accepted"
    except ValueError:
        pass
    return {"shortest_path_visit": n, "empty": empty}
def main():
    rec={"schema":"tourlock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"4-node tour length 4; empty graph is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["shortest_path_visit"]!=4 or rec["ours"]["empty"]!="raised":
        raise SystemExit("tourlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
