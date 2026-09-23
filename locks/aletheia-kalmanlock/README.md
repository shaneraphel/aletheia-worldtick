# Kalmanlock

Kalman observation occupancy on an autonomous-driving tape. Empty
observations are absence. They are not state 0.


## Problems

1. **Empty observation tape.** A tracker with no observations must refuse. It does not write state 0.
2. **A non-positive observation count.** Occupancy is not a missing covariance.
3. **The same tape twice.** `kalman_filter([(2,0),(3,1),(1,0)])` is 3 on two walks.

## Run

```bash
python3.12 kalmanlock.py --verify-precision
python3.12 kalman_bench.py
python3.12 show_filterpy.py
```

## Show

FilterPy on an observation tape. Their `update(None)` is accepted.
This kernel refuses an empty tape. See `SHOW.md`.

## Evidence

Pinned `python3.12 kalman_bench.py`. Numbers are copied from `results/KALMAN_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `kalman_filter` median | 0.00023762499768054113 s |
| naive median | 0.00029916700077592395 s |
| occupancy (twice) | 4096 |

## License

MIT
