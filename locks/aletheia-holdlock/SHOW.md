# Show: I used NetworkX, and I refused a missing pair row

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on four
seats: the same 1 swap so every couple sits together, plus a refusal when
the row is missing.

NetworkX 3.6.1 empty matching is `set()`.
`min_swaps_couples(None)` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
