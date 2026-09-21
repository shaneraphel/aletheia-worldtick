# Cyclelock

Floyd cycle occupancy on a next-pointer tape. Empty next is absence.
An acyclic walk is a measured 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `floyd.py`.

## Problems

1. **Empty next tape.** A world-model loop detector with no pointers must refuse.
2. **The same cycle twice.** `floyd_cycle([1,2,0])` is 1 on two walks.

## Run

```bash
python3.12 cyclelock.py --verify-precision
python3.12 floyd_bench.py
python3.12 show_networkx.py
```

## Show

I used NetworkX on the same three-node loop. Their empty `simple_cycles` is `[]`.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 floyd_bench.py`. Numbers are copied from `results/FLOYD_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `floyd_cycle` median | 0.0010776660019473638 s |
| set-walk median | 0.0006888749994686805 s |
| cycle (twice) | 1 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
