# Twistlock

Givens hypot and Householder first-entry on integer frames. An empty vector is
absence. A zero vector is absence. A non-square radius is absence. They are
not the identity rotation.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `givens.py` and `householder.py`.

## Problems

1. **Empty frame.** A wrist or camera rotation with no vector must refuse.
2. **Zero vector.** Stored DC is not a missing sample. The kernel raises.
3. **The same frames twice.** `givens_hypot([3,4])` is 5. `householder_first([3,4,12])` is -13.

## Run

```bash
python3.12 twistlock.py --verify-precision
python3.12 givens_bench.py
python3.12 householder_bench.py
python3.12 show_numpy.py
```

## Show

I used NumPy hypot on the same wrist frame. Their empty hypot is 0.0. This
kernel refuses. See `SHOW.md`.

## Evidence

Pinned seed 20260919. Numbers are copied from `results/GIVENS_EVIDENCE.json` and `results/HOUSEHOLDER_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| n_calls | 200000 |
| n_paired | 7 |
| `givens_hypot` median | 0.0391292499989504 s |
| `math.isqrt` median | 0.011235250000027008 s |
| hypot (twice) | 5 |
| `householder_first` median | 0.10658712499935064 s |
| naive median | 0.058758208997460315 s |
| first entry (twice) | -13 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
