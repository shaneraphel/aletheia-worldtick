# Sitelock

Fortune Voronoi-vertex occupancy on a site tape. Empty sites are absence.
They are not vertex count 0.


## Problems

1. **Empty site tape.** A world-model or contact Voronoi with no sites must refuse.
2. **The same sites twice.** `fortun_verts([(0,0),(2,0),(1,2)])` is 1 on two walks.

## Run

```bash
python3.12 sitelock.py --verify-precision
python3.12 fortun_bench.py
python3.12 show_scipy.py
```

## Show

SciPy `Voronoi` on the same three sites. Empty sites raise there.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 fortun_bench.py`. Numbers are copied from `results/FORTUN_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 24 |
| n_paired | 7 |
| `fortun_verts` median | 0.009291374997701496 s |
| vertices (twice) | 39 |

## License

MIT
