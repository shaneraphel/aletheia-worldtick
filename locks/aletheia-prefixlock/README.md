# Prefixlock

Fenwick prefix occupancy on a spike or lane-count tape. Empty values
are absence. They are not prefix 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `fenwick.py`.

## Problems

1. **Empty value tape.** A BCI spike prefix or lane count with no values must refuse.
2. **The same prefix twice.** `fenwick_prefix([1,2,3,4], 3)` is 10 on two walks.

## Run

```bash
python3.12 prefixlock.py --verify-precision
python3.12 fenwick_bench.py
python3.12 show_numpy.py
```

## Show

I used NumPy `cumsum` on the same four-bin prefix. Their empty `cumsum` is `[]`.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 fenwick_bench.py`. Numbers are copied from `results/FENWICK_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 65536 |
| n_paired | 7 |
| `fenwick_prefix` median | 0.11244587499822956 s |
| naive median | 0.00051875000281143 s |
| prefix (twice) | 229031 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
