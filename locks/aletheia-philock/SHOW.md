# Show: I used NetworkX, and I refused the empty CFG

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on a
3-block join: the same 1 φ site, plus a refusal when the CFG is empty.

NetworkX 3.6.1 empty Graph has no nodes.
`ssa_phi_count(0, [])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
