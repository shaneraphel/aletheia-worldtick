# Show: I used NetworkX, and I refused the empty fact tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [networkx/networkx](https://github.com/networkx/networkx) on a
3-node world: the same reach 3, plus a refusal when facts are empty.

NetworkX 3.6.1 `descendants` on an isolated node is `set()`.
`datalog_fixpoint(3, [], [(0,1)])` raises.

```bash
python3.12 show_networkx.py
```

Pinned output: `results/SHOW_NETWORKX.json`.
