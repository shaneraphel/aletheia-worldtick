# Camlock

Camera-cover occupancy on a dexterous-hand kinematic tree. A missing tree is
absence. It is not cover 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `camtree.py`.

## Problems

1. **A missing tree.** Sensor placement with no nodes must refuse. It does not write cover 0.
2. **The same one-node tree twice.** `min_camera_cover([0])` is 1 on two walks.

## Run

```bash
python3.12 camlock.py --verify-precision
python3.12 camtree_bench.py
python3.12 show_networkx.py
```

## Show

I used NetworkX on a one-node kinematic tree. Their empty Graph has no nodes.
`min_camera_cover(None)` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 camtree_bench.py`. Numbers are copied from `results/CAMTREE_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 64 |
| n_paired | 7 |
| `min_camera_cover` median | 2.3499997041653842e-05 s |
| repeat median | 2.3583001166116446e-05 s |
| cover (twice) | 19 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
