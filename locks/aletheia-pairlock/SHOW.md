# Show: I used NetworkX, and I refused the empty vertex set

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on a
four-finger pairing: the same matching 2, plus a refusal when `n<1`.

NetworkX 3.6.1 `maximal_matching` on an empty Graph is `set()`.
`blossom_match(0, [])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
