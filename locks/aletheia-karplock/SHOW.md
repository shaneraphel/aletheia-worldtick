# Show: I used NetworkX, and I refused the empty edge tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on a
2×2 grasp pairing: the same matching 2, plus a refusal when the edge tape
is empty.

NetworkX 3.6.1 `hopcroft_karp_matching` on two+two parts and no edges is 0.
`hopcroft_karp(2, 2, [])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
