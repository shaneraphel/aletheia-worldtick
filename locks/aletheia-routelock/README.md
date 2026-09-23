# Routelock

Johnson routing distance on a directed lane graph. An empty edge list is
absence. An unreachable destination is absence. A negative cycle is absence.
They are not distance 0.


## Problems

1. **Empty corridor.** A planner with no edges must refuse. It does not write distance 0.
2. **A negative cycle.** A ghost loop that cheapens forever is absence.
3. **The same path twice.** `johnson_dist(3, [(0,1,1),(1,2,1)], 0, 2)` is 2 on two walks.

## Run

```bash
python3.12 routelock.py --verify-precision
python3.12 johnson_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX on the same three-node lane. Their empty `johnson` is `{}`.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 johnson_bench.py`. Numbers are copied from `results/JOHNSON_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 64 |
| n_edges | 192 |
| n_paired | 7 |
| `johnson_dist` median | 0.000372874997992767 s |
| Dijkstra median | 3.0250001145759597e-05 s |
| dist (twice) | 5 |

## License

MIT
