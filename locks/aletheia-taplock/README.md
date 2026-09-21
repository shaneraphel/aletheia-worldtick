# Taplock

Garden-tap occupancy on an embodiment coverage tape. A missing width is
absence. It is not tap 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `tapsg.py`.

## Problems

1. **A missing garden width.** `n < 1` must refuse. It does not write tap 0.
2. **The same width-5 garden twice.** `min_taps(5, [3,4,1,1,0,0])` is 1 on two walks.

## Run

```bash
python3.12 taplock.py --verify-precision
python3.12 tapsg_bench.py
python3.12 show_numpy.py
```

## Show

I used NumPy on the same width-5 garden. Their empty `sum` is 0.0.
`min_taps(0, [])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 tapsg_bench.py`. Numbers are copied from `results/TAPSG_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 5 |
| n_paired | 7 |
| `min_taps` median | 1.8749997252598405e-06 s |
| repeat median | 1.7920028767548501e-06 s |
| taps (twice) | 1 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
