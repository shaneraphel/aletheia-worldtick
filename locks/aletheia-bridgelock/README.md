# Bridgelock

Tarjan-bridge occupancy on a world-model lane graph. Empty edges are absence.
They are not 0 bridges.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `tarjan.py`.

## Problems

1. **Empty edge tape.** A lane graph with no edges must refuse. It does not write 0 bridges.
2. **The same triangle-plus-pending twice.** `n_bridges(4, [(0,1),(1,2),(2,0),(2,3)])` is 1 on two walks.
3. **A negative vertex count.** The kernel raises.

## Run

```bash
python3.12 bridgelock.py --verify-precision
python3.12 tarjan_bench.py
python3.12 show_networkx.py
```

## Show

I used NetworkX on a triangle plus a pending lane. Their empty Graph has `[]`
bridges. `n_bridges(4, [])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 tarjan_bench.py`. Numbers are copied from `results/TARJAN_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 64 |
| n_paired | 7 |
| `n_bridges` median | 8.270900070783682e-05 s |
| repeat median | 8.712500130059198e-05 s |
| bridges (twice) | 0 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
