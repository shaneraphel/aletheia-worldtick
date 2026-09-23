# Slotlock

Interval-overlap occupancy on a world-model slot tape. Empty intervals are
absence. They are not overlap 0.


## Problems

1. **Empty slot tape.** A world-model timeline with no intervals must refuse.
2. **The same point twice.** `interval_tree_overlap([(0,4),(2,6)], 3)` is 2 on two walks.

## Run

```bash
python3.12 slotlock.py --verify-precision
python3.12 interval_bench.py
python3.12 show_intervaltree.py
```

## Show

chaimleib/intervaltree on the same two slots. Their empty `at` is `[]`.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 interval_bench.py`. Numbers are copied from `results/INTERVAL_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `interval_tree_overlap` median | 0.0009870419999060687 s |
| naive median | 0.0001840839977376163 s |
| overlap (twice) | 217 |

## License

MIT
