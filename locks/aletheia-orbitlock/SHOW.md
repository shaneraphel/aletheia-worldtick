# Show: NetworkX (a missing vertex)

Compared with [networkx/networkx](https://github.com/networkx/networkx) on four
lane components: the same 2 orbits, plus a refusal when `n` is negative.

NetworkX 3.6.1 `number_connected_components` on an empty Graph is 0.
`DisjointSet(-1)` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
