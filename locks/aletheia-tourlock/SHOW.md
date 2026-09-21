# Show: I used NetworkX, and I refused the empty tour graph

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on a
4-node world: the same tour length 4, plus a refusal when the graph is empty.

NetworkX 3.6.1 empty Graph has no nodes.
`shortest_path_visit([])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
