# Layerlock

Kahn layer occupancy on a task graph. Negative `n` is absence. A cycle
is a measured 0.


## Problems

1. **Negative part size.** A grasp or lane schedule with no valid width must refuse.
2. **The same chain twice.** `kahn_layers(3, [(0,1),(1,2)])` is 3 on two walks.

## Run

```bash
python3.12 layerlock.py --verify-precision
python3.12 kahn_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX on the same three-node task chain. Their empty longest
path is 0. This kernel refuses a negative `n`. See `SHOW.md`.

## Evidence

Pinned `python3.12 kahn_bench.py`. Numbers are copied from `results/KAHN_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 256 |
| n_paired | 7 |
| `kahn_layers` median | 8.274999709101394e-05 s |
| naive median | 6.658299753325991e-05 s |
| layers (twice) | 0 |

## License

MIT
