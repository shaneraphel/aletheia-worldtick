# Handlock

Hungarian min-assignment on a contact-cost square. An empty cost matrix is
absence. A non-square matrix is absence. They are not assignment cost 0.


## Problems

1. **Empty cost matrix.** A grasp-to-contact assigner with no costs must refuse. It does not write cost 0.
2. **Non-square costs.** Finger count and contact count must match. A ragged table is absence.
3. **The same square twice.** `hungar_cost([[1,2],[2,1]])` is 2 on two walks.

## Run

```bash
python3.12 handlock.py --verify-precision
python3.12 hungar_bench.py
python3.12 show_munkres.py
```

## Show

Munkres on the same contact square. Their empty `[[]]` is `[]`. This
kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 hungar_bench.py`. Numbers are copied from `results/HUNGAR_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 8 |
| n_paired | 7 |
| `hungar_cost` median | 0.014876749999530148 s |
| brute-permutation median | 0.01829025000188267 s |
| cost (twice) | 2 |

## License

MIT
