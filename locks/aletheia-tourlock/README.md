# Tourlock

Visit-every-node occupancy on a world-model graph. An empty graph is
absence. It is not tour length 0.


## Problems

1. **Empty graph.** A tour with no nodes must refuse. It does not write length 0.
2. **The same four nodes twice.** `shortest_path_visit([[1,2,3],[0],[0],[0]])` is 4 on two walks.

## Run

```bash
python3.12 tourlock.py --verify-precision
python3.12 visitall_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX on the same four-node world. Their empty Graph has no nodes.
`shortest_path_visit([])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 visitall_bench.py`. Numbers are copied from `results/VISITALL_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_nodes | 4 |
| n_paired | 7 |
| `shortest_path_visit` median | 8.958006219472736e-06 s |
| repeat median | 9.000003046821803e-06 s |
| length (twice) | 4 |

## License

MIT
