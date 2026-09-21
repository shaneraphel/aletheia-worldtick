# Show: I used NetworkX, and I refused a negative part size

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on a
three-node task chain: the same 3 layers, plus a refusal when `n` is negative.

NetworkX 3.6.1 `dag_longest_path_length` on an empty DiGraph is 0.
`kahn_layers(-1, [])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
