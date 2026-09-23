# Sidelock

Left-visible occupancy on a world-model stick tape. A missing count is
absence. It is not 0 arrangements.


## Problems

1. **A missing stick count.** `n < 1` must refuse. It does not write 0 ways.
2. **The same three sticks twice.** `ways_rearrange_sticks(3, 2)` is 3 on two walks.

## Run

```bash
python3.12 sidelock.py --verify-precision
python3.12 visst_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on the same three-stick tape. Their empty `count_nonzero` is 0.
`ways_rearrange_sticks(0, 1)` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 visst_bench.py`. Numbers are copied from `results/VISST_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 8 |
| k | 4 |
| n_paired | 7 |
| `ways_rearrange_sticks` median | 8.125003660097718e-06 s |
| repeat median | 8.208000508602709e-06 s |
| ways (twice) | 6769 |

## License

MIT
