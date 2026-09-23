# Coinlock

Cheapest coin-path occupancy on an autonomous-driving toll tape. A missing
coin row is absence. It is not an empty path.


## Problems

1. **A missing coin row.** `cheapest_jump([], 2)` must refuse. It does not write `[]`.
2. **The same five coins twice.** `cheapest_jump([1,2,4,-1,2], 2)` is `[1,3,5]` on two walks.

## Run

```bash
python3.12 coinlock.py --verify-precision
python3.12 coinp_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX on the same five coins. Their empty digraph has 0 nodes.
`cheapest_jump([], 2)` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 coinp_bench.py`. Numbers are copied from `results/COINP_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_coins | 5 |
| n_paired | 7 |
| `cheapest_jump` median | 2.7080022846348584e-06 s |
| repeat median | 2.749999111983925e-06 s |
| path (twice) | [1, 3, 5] |

## License

MIT
