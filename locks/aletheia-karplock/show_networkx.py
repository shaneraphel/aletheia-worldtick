#!/usr/bin/env python3.12
"""Use NetworkX Hopcroft–Karp on a grasp pairing. Record empty edges. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from hopcroft import hopcroft_karp


def theirs() -> dict:
    import networkx as nx

    empty = nx.Graph()
    empty.add_nodes_from([0, 1], bipartite=0)
    empty.add_nodes_from(["a", "b"], bipartite=1)
    paired = nx.Graph()
    paired.add_nodes_from([0, 1], bipartite=0)
    paired.add_nodes_from(["a", "b"], bipartite=1)
    paired.add_edges_from([(0, "a"), (0, "b"), (1, "b")])
    return {
        "package": "networkx",
        "version": nx.__version__,
        "empty_matching": len(nx.bipartite.hopcroft_karp_matching(empty, top_nodes=[0, 1])) // 2,
        "paired_matching": len(nx.bipartite.hopcroft_karp_matching(paired, top_nodes=[0, 1])) // 2,
    }


def ours() -> dict:
    m = hopcroft_karp(2, 2, [(0, 0), (0, 1), (1, 1)])
    empty = "raised"
    try:
        hopcroft_karp(2, 2, [])
        empty = "accepted"
    except ValueError:
        pass
    return {"hopcroft_paired": m, "empty": empty}


def main() -> int:
    rec = {
        "schema": "karplock.show_networkx.v1",
        "used": "https://github.com/networkx/networkx",
        "built": "2x2 grasp pairing matching 2; empty edges are absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["hopcroft_paired"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("karplock show identity failed")
    if rec["theirs"]["paired_matching"] != 2:
        raise SystemExit("networkx pairing identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
