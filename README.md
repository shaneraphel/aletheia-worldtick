# Worldtick

Fact reachability for a discrete world tick. Empty facts are absence. They
are not "zero reachable". A negative world width is absence.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `datalog.py` and `policy.py`.

## Problems

1. **Empty fact tape.** A world with no occupied facts must refuse. It does not write reach 0.
2. **The same facts twice.** `datalog_fixpoint` returns the same reach count on two walks.
3. **A cited world.** Seed, n_nodes, n_facts, and n_edges are pinned in the bench JSON.
4. **Empty reward table.** `policy_iteration` refuses. It does not write action 0.

## Run

```bash
python3.12 worldtick.py --verify-precision
python3.12 datalog_bench.py
python3.12 policy_bench.py
```

## Kernels

- `datalog.py` — Datalog fixpoint reachability
- `policy.py` — policy iteration on a reward table

## Show

I used NetworkX on the same 3-node world. Their empty Graph has no nodes.
This kernel refuses empty facts. See `SHOW.md`.

```bash
python3.12 show_networkx.py
```

## Evidence

Pinned `python3.12 datalog_bench.py`. Numbers are copied from `results/DATALOG_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_nodes | 256 |
| n_facts | 8 |
| n_edges | 512 |
| n_paired | 7 |
| `datalog_fixpoint` median | 0.0003089579986408353 s |
| BFS reach median | 0.0001294169924221933 s |
| reach (twice) | 214 |
| n_states | 256 |
| n_actions | 8 |
| `policy_iteration` median | 0.0005760419880971313 s |
| row-0 greedy median | 1.4579854905605316e-06 s |
| action (twice) | 4 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT

## Atlas

100 small `*-bind` libraries, 66 `*-lock` kernels, 10 resource lists, and 6 small
tools now live in this repo under `binds/`, `locks/`, `docs-awesome/`, and `tools/`.
See `ATLAS.md` for the full index. Each subdirectory keeps the files of its
former standalone repository.
