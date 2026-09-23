# Orbitlock

Disjoint-set occupancy on an autonomous-driving lane tape. A negative vertex
count is absence. It is not 0 components.


## Problems

1. **A negative vertex count.** Lane merge with `n < 0` must refuse. It does not write 0 orbits.
2. **The same four nodes twice.** `DisjointSet(4).union(0,1).union(2,3).n_orbits()` is 2 on two walks.
3. **A missing vertex.** `find(-1)` raises.

## Run

```bash
python3.12 orbitlock.py --verify-precision
python3.12 orbits_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX on four lane nodes. Their empty Graph has 0 components.
`DisjointSet(-1)` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 orbits_bench.py`. Numbers are copied from `results/ORBITS_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `n_orbits` median | 0.004201750001811888 s |
| naive median | 0.0024897500006773043 s |
| orbits (twice) | 637 |

## License

MIT
