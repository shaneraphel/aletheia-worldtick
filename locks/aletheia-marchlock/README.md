# Marchlock

Jarvis-march hull occupancy on a contact-point tape. Empty points are
absence. They are not hull size 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `jarvis.py`.

## Problems

1. **Empty point tape.** A grasp hull with no contacts must refuse.
2. **The same points twice.** `jarvis_hull([(0,0),(2,0),(1,1),(0,2),(2,2)])` is 4 on two walks.

## Run

```bash
python3.12 marchlock.py --verify-precision
python3.12 jarvis_bench.py
python3.12 show_scipy.py
```

## Show

I used SciPy `ConvexHull` on the same five contacts. Empty points raise there.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 jarvis_bench.py`. Numbers are copied from `results/JARVIS_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `jarvis_hull` median | 0.01779624999835505 s |
| Graham median | 0.0026663329990697093 s |
| hull (twice) | 21 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
