# Lcplock

Kasai LCP at an index on a text and suffix array. Empty text and a bad
index are absence. They are not LCP 0.


## Problems

1. **Empty suffix tape.** A spike-pattern or route string with no text must refuse.
2. **The same index twice.** `kasai_lcp_at("banana", [5,3,1,0,4,2], 2)` is 3 on two walks.

## Run

```bash
python3.12 lcplock.py --verify-precision
python3.12 kasai_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on the same `banana` suffixes. Their empty compare is 0. This
kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 kasai_bench.py`. Numbers are copied from `results/KASAI_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 1024 |
| n_paired | 7 |
| `kasai_lcp_at` median | 0.0007397499975922983 s |
| naive median | 1.791999238776043e-06 s |
| LCP (twice) | 2 |

## License

MIT
