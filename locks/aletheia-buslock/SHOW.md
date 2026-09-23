# Show: NetworkX (missing routes)

Compared with [networkx/networkx](https://github.com/networkx/networkx) on two
city routes: the same 2 buses, plus a refusal when the route table is missing.

NetworkX 3.6.1 `shortest_path` on an empty Graph raises.
`num_buses(None, 1, 6)` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
