# Woodlock

Forest-cut occupancy on a world-model height field. An empty forest is
absence. It is not step 0.


## Problems

1. **Empty forest.** A cutter with no cells must refuse. It does not write step 0.
2. **The same 3×3 forest twice.** `cut_off_trees([[1,2,3],[0,0,4],[7,6,5]])` is 6 on two walks.

## Run

```bash
python3.12 woodlock.py --verify-precision
python3.12 cuttre_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on the same 3×3 forest. Their empty `norm` is 0.0.
`cut_off_trees([])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 cuttre_bench.py`. Numbers are copied from `results/CUTTRE_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_rows | 3 |
| n_cols | 3 |
| n_paired | 7 |
| `cut_off_trees` median | 6.750000466126949e-06 s |
| repeat median | 6.583002686966211e-06 s |
| steps (twice) | 6 |

## License

MIT
