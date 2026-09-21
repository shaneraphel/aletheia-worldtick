# Lanelock

Occupancy-cycle and planning-layer kernels for a next-pose tape. An empty
next tape is absence. It is not "acyclic 0". A negative node count is
absence. It is not "zero layers".

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `floyd.py` and `kahn.py`.

## Problems

1. **Empty next-pose tape.** A tracker with no successor list must refuse. It does not write "no loop".
2. **A pose loop on the tape.** `floyd_cycle` returns 1 or 0. The same tape answers twice.
3. **Empty planning width.** `kahn_layers` refuses a negative node count. A DAG with a cycle returns 0 layers after a full walk.

## Run

```bash
python3.12 lanelock.py --verify-precision
python3.12 floyd_bench.py
python3.12 kahn_bench.py
python3.12 show_networkx.py
```

## Show

I used NetworkX on the same pose loop. Their empty `simple_cycles` is `[]`.
This kernel refuses. See `SHOW.md`.

## Kernels

- `floyd.py` — Floyd cycle on a next-pose tape
- `kahn.py` — Kahn layer assignment on a planning DAG

## Evidence

Pinned seed 20260919. Numbers are copied from `results/FLOYD_EVIDENCE.json` and `results/KAHN_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| n (floyd) | 65536 |
| n_paired | 7 |
| `floyd_cycle` median | 7.70896440371871e-06 s |
| set-walk median | 4.332978278398514e-06 s |
| cycle (twice) | 1 |
| n_nodes (kahn) | 256 |
| n_edges | 512 |
| `kahn_layers` median | 0.00012804201105609536 s |
| BFS layers median | 0.00012637500185519457 s |
| layers (twice) | 18 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
