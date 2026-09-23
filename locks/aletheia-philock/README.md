# Philock

SSA φ occupancy on a control-flow join. An empty CFG is absence. It is
not zero φ sites.


## Problems

1. **Empty CFG.** A missing predecessor tape must refuse.
2. **A join with two predecessors.** That block occupies one φ site.
3. **The same CFG twice.** `ssa_phi_count` returns the same count on two walks.

## Run

```bash
python3.12 philock.py --verify-precision
python3.12 ssa_bench.py
```

## Show

NetworkX on the same 3-block join. Their empty Graph has no nodes.
This kernel refuses an empty CFG. See `SHOW.md`.

```bash
python3.12 show_networkx.py
```

## Evidence

Pinned `python3.12 ssa_bench.py`. Numbers are copied from `results/SSA_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 512 |
| n_paired | 7 |
| `ssa_phi_count` median | 9.32919792830944e-05 s |
| naive join count median | 9.916024282574654e-06 s |
| n_phi (twice) | 125 |

## License

MIT
