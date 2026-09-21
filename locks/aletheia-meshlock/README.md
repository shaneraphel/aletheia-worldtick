# Meshlock

Delaunay triangle occupancy on a contact-site tape. Empty sites are absence.
Fewer than three unique sites is a real count of 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `delaun.py`.

## Problems

1. **Empty site tape.** A contact mesh with no sites must refuse.
2. **The same sites twice.** `delaun_tris([(0,0),(2,0),(1,1),(0,2),(2,2)])` is 4 on two walks.

## Run

```bash
python3.12 meshlock.py --verify-precision
python3.12 delaun_bench.py
python3.12 show_scipy.py
```

## Show

I used SciPy `Delaunay` on the same five sites. Empty sites raise there.
This kernel refuses, and the mesh is 4 triangles. See `SHOW.md`.

## Evidence

Pinned `python3.12 delaun_bench.py`. Numbers are copied from `results/DELAUN_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 256 |
| n_paired | 7 |
| `delaun_tris` median | 0.0005092079991300125 s |
| formula median | 0.0005383749994507525 s |
| triangles (twice) | 494 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
