# Celllock

Voronoi unbounded-cell occupancy on a site tape. Empty sites are absence.
They are not cell count 0.


## Problems

1. **Empty site tape.** A world-cell diagram with no sites must refuse.
2. **The same sites twice.** `voronoi_unbounded([(0,0),(2,0),(1,1),(0,2),(2,2)])` is 4 on two walks.

## Run

```bash
python3.12 celllock.py --verify-precision
python3.12 voronoi_bench.py
python3.12 show_scipy.py
```

## Show

SciPy `Voronoi` on the same five world-model sites. Empty sites raise
there. This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 voronoi_bench.py`. Numbers are copied from `results/VORONOI_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `voronoi_unbounded` median | 0.0026342909986851737 s |
| hull median | 0.0026052079992950894 s |
| cells (twice) | 21 |

## License

MIT
