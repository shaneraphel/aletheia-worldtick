# Show: NetworkX (the empty edge tape)

Compared with [networkx/networkx](https://github.com/networkx/networkx) on a
triangle-plus-pending lane: the same 1 bridge, plus a refusal when the
edge tape is empty.

NetworkX 3.6.1 `bridges` on an empty Graph is `[]`.
`n_bridges(4, [])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
