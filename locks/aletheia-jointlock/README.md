# Jointlock

Two-link inverse kinematics. Unreachable targets are refusal. They are
not rest-pose zero.


## Problems

1. **Unreachable pose.** A dexterous-hand target outside the annulus must refuse.
2. **The same reach twice.** `two_link_ik(2.0, 0.0, 1.0, 1.0)` is a 2-tuple on two walks.

## Run

```bash
python3.12 jointlock.py --verify-precision
python3.12 ik_bench.py
python3.12 show_numpy.py
```

## Show

NumPy on the same two-link reach. Their empty `norm` is 0.0. This
kernel refuses an unreachable pose. See `SHOW.md`.

## Evidence

Pinned `python3.12 ik_bench.py`. Numbers are copied from `results/IK_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 20000 |
| n_paired | 7 |
| `two_link_ik` median | 0.027457041000161553 s |
| law-of-cosines median | 0.020422458997927606 s |
| poses (twice) | 20000 |

## License

MIT
