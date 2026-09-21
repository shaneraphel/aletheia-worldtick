#!/usr/bin/env python3.12
"""Use NetworkX layers on a task chain. Record empty DAG. Refuse negative n."""

from __future__ import annotations

import json
import platform
import sys

from kahn import kahn_layers


def theirs() -> dict:
    import networkx as nx

    empty_len = nx.dag_longest_path_length(nx.DiGraph())
    chain = nx.DiGraph([(0, 1), (1, 2)])
    gens = [list(g) for g in nx.topological_generations(chain)]
    return {
        "package": "networkx",
        "version": nx.__version__,
        "empty_longest_path": empty_len,
        "chain_generations": len(gens),
    }


def ours() -> dict:
    layers = kahn_layers(3, [(0, 1), (1, 2)])
    negative = "raised"
    try:
        kahn_layers(-1, [])
        negative = "accepted"
    except ValueError:
        pass
    return {"kahn_chain": layers, "negative_n": negative}


def main() -> int:
    rec = {
        "schema": "layerlock.show_networkx.v1",
        "used": "https://github.com/networkx/networkx",
        "built": "three-node task chain 3 layers; negative n is absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["kahn_chain"] != 3 or rec["ours"]["negative_n"] != "raised":
        raise SystemExit("layerlock show identity failed")
    if rec["theirs"]["chain_generations"] != 3:
        raise SystemExit("networkx chain identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
