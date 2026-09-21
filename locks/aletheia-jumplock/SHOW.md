# Show: I used NetworkX, and I refused empty stones

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on eight
compiled stones: the frog crosses, and an empty stone tape refuses.

NetworkX `Graph()` has 0 nodes and 0 components.
`can_cross([])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
