# Cliplock

Akl–Toussaint interior discard on a contact tape. Empty points are absence.
They are not discard count 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `aktous.py`.

## Problems

1. **Empty point tape.** A hull prefilter with no contacts must refuse.
2. **The same square twice.** `aktous_discard([(0,0),(2,0),(1,1),(0,2),(2,2)])` is 1 on two walks.

## Run

```bash
python3.12 cliplock.py --verify-precision
python3.12 aktous_bench.py
python3.12 show_scipy.py
```

## Show

I used SciPy `ConvexHull` on the same five contacts. Empty points raise there.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 aktous_bench.py`. Numbers are copied from `results/AKTOUS_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 65536 |
| n_paired | 7 |
| `aktous_discard` median | 0.004055124998558313 s |
| naive median | 0.004148957999859704 s |
| discarded (twice) | 61590 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
