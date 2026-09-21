# Climblock

Longest increasing path on a world-model height field. An empty field is
absence. It is not path 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `lipath.py`.

## Problems

1. **Empty height field.** A climb with no cells must refuse. It does not write path 0.
2. **The same 3×3 field twice.** `longest_increasing_path([[9,9,4],[6,6,8],[2,1,1]])` is 4 on two walks.

## Run

```bash
python3.12 climblock.py --verify-precision
python3.12 lipath_bench.py
python3.12 show_numpy.py
```

## Show

I used NumPy on the same 3×3 field. Their empty `max` raises.
`longest_increasing_path([])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 lipath_bench.py`. Numbers are copied from `results/LIPATH_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 8 |
| n_paired | 7 |
| `longest_increasing_path` median | 7.050000203889795e-05 s |
| repeat median | 7.208299939520657e-05 s |
| path (twice) | 7 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
