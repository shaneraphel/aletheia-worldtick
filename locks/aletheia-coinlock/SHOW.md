# Show: I used NetworkX, and I refused an empty coin row

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on five
toll coins: the same 1-3-5 path, plus a refusal when the coin row is empty.

NetworkX `DiGraph()` has 0 nodes.
`cheapest_jump([], 2)` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
