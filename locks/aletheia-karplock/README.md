# Karplock

Hopcroft–Karp matching occupancy on a bipartite edge tape. Empty edges
are absence. They are not matching size 0.


## Problems

1. **Empty edge tape.** A grasp or lane pairing with no edges must refuse.
2. **The same graph twice.** `hopcroft_karp(2, 2, [(0,0),(0,1),(1,1)])` is 2 on two walks.

## Run

```bash
python3.12 karplock.py --verify-precision
python3.12 hopcroft_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX Hopcroft–Karp on the same 2×2 pairing. Their empty matching is 0.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 hopcroft_bench.py`. Numbers are copied from `results/HOPCROFT_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 80 |
| n_paired | 7 |
| `hopcroft_karp` median | 0.0003275829985796008 s |
| greedy median | 7.308299973374233e-05 s |
| matching (twice) | 80 |

## License

MIT
