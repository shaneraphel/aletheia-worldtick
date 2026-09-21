# Hulllock

Graham-scan hull occupancy on a contact-point tape. Empty points are
absence. They are not hull size 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `graham.py`.

## Problems

1. **Empty point tape.** A grasp or bumper hull with no contacts must refuse.
2. **Interior points.** `graham_hull([(0,0),(2,0),(1,1),(0,2),(2,2)])` is 4 on two walks.
3. **Two points.** `graham_hull([(0,0),(1,0)])` is 2, a real count.

## Run

```bash
python3.12 hulllock.py --verify-precision
python3.12 graham_bench.py
python3.12 show_scipy.py
```

## Show

I used SciPy `ConvexHull` on the same five contacts. Empty points raise there.
This kernel refuses, and the hull is 4. See `SHOW.md`.

## Evidence

Pinned `python3.12 graham_bench.py`. Numbers are copied from `results/GRAHAM_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `graham_hull` median | 0.009089459003007505 s |
| Jarvis median | 0.041086499997618375 s |
| hull (twice) | 21 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
