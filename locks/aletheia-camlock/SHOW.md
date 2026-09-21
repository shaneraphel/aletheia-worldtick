# Show: I used NetworkX, and I refused the empty camera tree

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on a
one-node kinematic tree: the same 1 camera, plus a refusal when the tree
is missing.

NetworkX 3.6.1 empty Graph has no nodes.
`min_camera_cover(None)` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
