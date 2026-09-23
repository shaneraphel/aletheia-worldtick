# Show: NetworkX (the empty next-pose tape)

Compared with [networkx/networkx](https://github.com/networkx/networkx) on a
three-node pose loop: occupancy 1 here, plus a refusal when the next tape
is empty.

NetworkX 3.6.1 `simple_cycles` on an empty DiGraph is `[]`.
`floyd_cycle([])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
