# Show: I used Munkres, and I refused the empty cost

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [bmc/munkres](https://github.com/bmc/munkres) on a dexterous-hand
contact square: the same 2×2 assignment, plus a refusal when the cost tape is
empty.

`munkres` 1.1.4 on `[[]]` returns `[]`. That is not a measured assignment.
`hungar_cost([])` raises. The note on their tree is
[bmc/munkres#54](https://github.com/bmc/munkres/issues/54).

```bash
python3.12 show_munkres.py
```

Pinned output: `results/SHOW_MUNKRES.json`.
