#!/usr/bin/env python3.12
"""Use NetworkX descendants on a world tick. Record empty facts. Refuse here."""
from __future__ import annotations
import json, platform, sys
from datalog import datalog_fixpoint

def theirs() -> dict:
    import networkx as nx
    empty = list(nx.descendants(nx.DiGraph(), 0)) if False else list(nx.DiGraph().nodes())
    g = nx.DiGraph([(0,1),(1,2)])
    reach = {0} | nx.descendants(g, 0)
    return {"package":"networkx","version":nx.__version__,"empty_nodes":empty,"n_reach": len(reach)}

def ours() -> dict:
    n = datalog_fixpoint(3, [0], [(0,1),(1,2)])
    empty = "raised"
    try:
        datalog_fixpoint(3, [], [(0,1)])
        empty = "accepted"
    except ValueError:
        pass
    return {"datalog_fixpoint": n, "empty": empty}

def main() -> int:
    rec = {"schema":"worldtick.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"3-node world reach 3; empty facts are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["datalog_fixpoint"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("worldtick show identity failed")
    if rec["theirs"]["n_reach"] != 3:
        raise SystemExit("networkx reach identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
