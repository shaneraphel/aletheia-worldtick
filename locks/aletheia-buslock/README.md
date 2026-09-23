# Buslock

Fewest buses on an autonomous-driving route table. A missing table is
absence. It is not hop 0.


## Problems

1. **A missing route table.** A transfer planner with no routes must refuse. It does not write hop 0.
2. **The same two routes twice.** `num_buses([[1,2,7],[3,6,7]], 1, 6)` is 2 on two walks.

## Run

```bash
python3.12 buslock.py --verify-precision
python3.12 busrts_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX on the same two city routes. Their empty `shortest_path` raises.
`num_buses(None, 1, 6)` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 busrts_bench.py`. Numbers are copied from `results/BUSRTS_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 8 |
| n_paired | 7 |
| `num_buses` median | 5.292000423651189e-06 s |
| repeat median | 5.375000910134986e-06 s |
| hops (twice) | 1 |

## License

MIT
