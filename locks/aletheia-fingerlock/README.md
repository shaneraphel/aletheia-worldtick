# Fingerlock

Two-finger occupancy on a dexterous-hand letter tape. An empty word is
absence. It is not distance 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `twofng.py`.

## Problems

1. **Empty finger tape.** Two fingers with no letters must refuse. They do not write distance 0.
2. **The same word twice.** `minimum_distance("CAKE")` is 3 on two walks.

## Run

```bash
python3.12 fingerlock.py --verify-precision
python3.12 twofng_bench.py
python3.12 show_numpy.py
```

## Show

I used NumPy on `CAKE`. Their empty `norm` is 0.0.
`minimum_distance("")` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 twofng_bench.py`. Numbers are copied from `results/TWOFNG_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 8 |
| n_paired | 7 |
| `minimum_distance` median | 3.7500001781154424e-05 s |
| repeat median | 3.749999814317562e-05 s |
| distance (twice) | 12 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
