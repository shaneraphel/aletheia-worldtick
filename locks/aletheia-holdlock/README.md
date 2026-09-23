# Holdlock

Couple-swap occupancy on a dexterous-hand seat row. A missing row is
absence. It is not swap 0.


## Problems

1. **A missing seat row.** Pairing with no row must refuse. It does not write swap 0.
2. **The same four seats twice.** `min_swaps_couples([0,2,1,3])` is 1 on two walks. Already-paired `[3,2,0,1]` is 0.

## Run

```bash
python3.12 holdlock.py --verify-precision
python3.12 couple_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX on four seats. Their empty matching is `set()`.
`min_swaps_couples(None)` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 couple_bench.py`. Numbers are copied from `results/COUPLE_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 64 |
| n_paired | 7 |
| `min_swaps_couples` median | 1.0750001820269972e-05 s |
| repeat median | 1.0792002285597846e-05 s |
| swaps (twice) | 29 |

## License

MIT
