# Show: I used NetworkX, and I refused the empty next tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on a
three-node world-model loop: the same cycle occupancy 1, plus a refusal when
the next tape is empty.

NetworkX 3.6.1 `simple_cycles` on an empty DiGraph is `[]`.
`floyd_cycle([])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
