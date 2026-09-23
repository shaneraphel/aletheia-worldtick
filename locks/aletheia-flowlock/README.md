# Flowlock

Dinic blocking-flow occupancy on a residual graph. Empty edges are
absence. They are not flow 0.


## Problems

1. **Empty residual tape.** A traffic or blood-flow graph with no edges must refuse.
2. **The same graph twice.** `dinic_max_flow(4, [(0,1,1),(0,2,1),(1,3,1),(2,3,1)], 0, 3)` is 2 on two walks.

## Run

```bash
python3.12 flowlock.py --verify-precision
python3.12 dinic_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX on the same traffic diamond. Their empty residual is flow 0.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 dinic_bench.py`. Numbers are copied from `results/DINIC_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 24 |
| n_paired | 7 |
| `dinic_max_flow` median | 0.00017391600340488367 s |
| Ford–Fulkerson median | 0.00011054200149374083 s |
| flow (twice) | 12 |

## License

MIT
