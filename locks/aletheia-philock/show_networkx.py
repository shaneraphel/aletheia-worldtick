#!/usr/bin/env python3.12
"""Use NetworkX on a 3-block join. Record empty CFG. Refuse here."""
from __future__ import annotations
import json, platform, sys
from ssa import ssa_phi_count

def theirs() -> dict:
    import networkx as nx
    empty = list(nx.DiGraph().nodes())
    g = nx.DiGraph()
    g.add_nodes_from(range(3))
    g.add_edges_from([(0,2),(1,2)])
    joins = sum(1 for n in g.nodes() if g.in_degree(n) >= 2)
    return {"package":"networkx","version":nx.__version__,"empty_nodes":empty,"n_joins": joins}

def ours() -> dict:
    n = ssa_phi_count(3, [[], [], [0, 1]])
    empty = "raised"
    try:
        ssa_phi_count(0, [])
        empty = "accepted"
    except ValueError:
        pass
    return {"ssa_phi_count": n, "empty": empty}

def main() -> int:
    rec = {"schema":"philock.show_networkx.v1","used":"https://github.com/networkx/networkx","built":"3-block join occupies 1 phi site; empty CFG is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["ssa_phi_count"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("philock show identity failed")
    if rec["theirs"]["n_joins"] != 1:
        raise SystemExit("networkx join identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
