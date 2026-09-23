# Spanlock

Segment-tree range sum on a count tape. Empty arrays and a bad range are
absence. They are not sum 0.


## Problems

1. **Empty count tape.** A BEV or spike window with no values must refuse.
2. **The same range twice.** `segspt_sum([1,3,5,7,9], 1, 3)` is 15 on two walks.

## Run

```bash
python3.12 spanlock.py --verify-precision
python3.12 segspt_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on the same window. Their empty `sum` is 0.0. This kernel
refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 segspt_bench.py`. Numbers are copied from `results/SEGSPT_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `segspt_sum` median | 0.0025472909983363934 s |
| naive median | 4.587500006891787e-05 s |
| sum (twice) | 14133 |

## License

MIT
