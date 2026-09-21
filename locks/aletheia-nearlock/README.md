# Nearlock

Nearest-x after inserts on a contact tape. Empty points are absence. They
are not coordinate 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `kdtree.py`.

## Problems

1. **Empty contact tape.** A nearest-finger query with no points must refuse.
2. **The same query twice.** `kdtree_near([(0,0),(3,4)], 3, 4)` is 3 on two walks.

## Run

```bash
python3.12 nearlock.py --verify-precision
python3.12 kdtree_bench.py
python3.12 show_kdtree.py
```

## Show

I used stefankoegl/kdtree on the same contacts. Empty `search_nn` is `None`
there. This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 kdtree_bench.py`. Numbers are copied from `results/KDTREE_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 65536 |
| n_paired | 7 |
| `kdtree_near` median | 0.01804983400143101 s |
| naive median | 0.017401249999238644 s |
| x (twice) | 41260 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
