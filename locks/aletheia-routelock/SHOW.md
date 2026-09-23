# Show: NetworkX (the empty corridor)

Compared with [networkx/networkx](https://github.com/networkx/networkx) on a
three-node lane: the same distance 2, plus a refusal when the edge tape
is empty.

NetworkX 3.6.1 `johnson` on an empty DiGraph is `{}`.
`johnson_dist(3, [], 0, 2)` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
