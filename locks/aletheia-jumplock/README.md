# Jumplock

Frog-jump occupancy on an embodiment foothold tape. Missing stones are
absence. They are not cannot-cross.


## Problems

1. **A missing stone tape.** `can_cross([])` must refuse. It does not write False.
2. **The same eight stones twice.** `can_cross([0,1,3,5,6,8,12,17])` is True on two walks.

## Run

```bash
python3.12 jumplock.py --verify-precision
python3.12 frogjp_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX on the same eight stones. Their empty graph has 0 nodes.
`can_cross([])` raises. See `SHOW.md`.

## Evidence

Pinned `python3.12 frogjp_bench.py`. Numbers are copied from `results/FROGJP_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_stones | 8 |
| n_paired | 7 |
| `can_cross` median | 6.250003934837878e-06 s |
| repeat median | 6.083995685912669e-06 s |
| cross (twice) | True |

## License

MIT
