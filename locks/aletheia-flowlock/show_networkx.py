#!/usr/bin/env python3.12
"""Use NetworkX max-flow on a traffic diamond. Record empty residual. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from dinic import dinic_max_flow


def theirs() -> dict:
    import networkx as nx

    empty = nx.DiGraph()
    empty.add_nodes_from([0, 1, 2, 3])
    diamond = nx.DiGraph()
    diamond.add_edge(0, 1, capacity=1)
    diamond.add_edge(0, 2, capacity=1)
    diamond.add_edge(1, 3, capacity=1)
    diamond.add_edge(2, 3, capacity=1)
    return {
        "package": "networkx",
        "version": nx.__version__,
        "empty_residual_flow": nx.maximum_flow_value(empty, 0, 3),
        "diamond_flow": nx.maximum_flow_value(diamond, 0, 3),
    }


def ours() -> dict:
    flow = dinic_max_flow(4, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1)], 0, 3)
    empty = "raised"
    try:
        dinic_max_flow(4, [], 0, 3)
        empty = "accepted"
    except ValueError:
        pass
    return {"dinic_diamond": flow, "empty": empty}


def main() -> int:
    rec = {
        "schema": "flowlock.show_networkx.v1",
        "used": "https://github.com/networkx/networkx",
        "built": "four-node traffic diamond max-flow 2; empty residual is absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["dinic_diamond"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("flowlock show identity failed")
    if rec["theirs"]["diamond_flow"] != 2:
        raise SystemExit("networkx diamond identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
