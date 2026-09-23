# Show: NetworkX (the empty tour graph)

Compared with [networkx/networkx](https://github.com/networkx/networkx) on a
4-node world: the same tour length 4, plus a refusal when the graph is empty.

NetworkX 3.6.1 empty Graph has no nodes.
`shortest_path_visit([])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
