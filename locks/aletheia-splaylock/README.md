# Splaylock

Splay-to-root occupancy on a key tape. Empty trees and missing keys are
absence. They are not root 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `splay.py`.

## Problems

1. **Empty key tape.** A cache or contact tree with no keys must refuse.
2. **The same keys twice.** `splay_root([2,1,3], 1)` is 1 on two walks.

## Run

```bash
python3.12 splaylock.py --verify-precision
python3.12 splay_bench.py
```

## Show

I used grantjenks/python-sortedcontainers on the same three keys. Their empty
`SortedSet` membership is `False`. This kernel refuses. See `SHOW.md`.

```bash
python3.12 show_sortedcontainers.py
```

## Evidence

Pinned `python3.12 splay_bench.py`. Numbers are copied from `results/SPLAY_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `splay_root` median | 0.012656625000090571 s |
| `list.index` median | 2.2541000362252817e-05 s |
| root (twice) | 969 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
