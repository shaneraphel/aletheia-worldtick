# Voxelock

Octree north-east occupancy after one split. Empty points are absence. They
are not occupancy 0.


## Problems

1. **Empty voxel tape.** A lidar or body octree with no points must refuse.
2. **The NE child.** `octpart_ne([(1,1,1),(0,0,0)], 1, 1, 1)` is 1 on two walks.

## Run

```bash
python3.12 voxelock.py --verify-precision
python3.12 octpart_bench.py
python3.12 show_numpy.py
python3.12 show_nuscenes.py
```

## Show

NumPy on the same two lidar points. Their empty `norm` is 0.0. This
kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 octpart_bench.py`. Numbers are copied from `results/OCTPART_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 200000 |
| n_paired | 7 |
| `octpart_ne` median | 0.012522583001555176 s |
| naive median | 0.01416600000084145 s |
| NE (twice) | 25020 |

## License

MIT
