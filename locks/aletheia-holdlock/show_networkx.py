#!/usr/bin/env python3.12
"""Use NetworkX matching on four seats. Record empty matching. Refuse missing row."""
from __future__ import annotations
import json, platform, sys
from couple import min_swaps_couples

def theirs() -> dict:
    import networkx as nx
    empty=list(nx.max_weight_matching(nx.Graph(), maxcardinality=True))
    g=nx.Graph([(0,1),(2,3)])
    return {"package":"networkx","version":nx.__version__,"empty_matching":empty,"n_pairs":len(nx.max_weight_matching(g, maxcardinality=True))//2}

def ours() -> dict:
    n=min_swaps_couples([0,2,1,3])
    empty="raised"
    try:
        min_swaps_couples(None)
        empty="accepted"
    except ValueError:
        pass
    return {"min_swaps_couples":n,"empty":empty}

def main() -> int:
    rec={"schema":"holdlock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"four-seat couple swap 1; missing row is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["min_swaps_couples"]!=1 or rec["ours"]["empty"]!="raised":
        raise SystemExit("holdlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
