# Treaplock

Treap-root occupancy on a key and priority tape. Empty tapes and length
mismatch are absence. They are not root 0.


## Problems

1. **Empty or ragged tape.** A cache or contact treap with no keys must refuse.
2. **The same tapes twice.** `treap_root([5,3,8], [2,4,1])` is 3 on two walks.

## Run

```bash
python3.12 treaplock.py --verify-precision
python3.12 treap_bench.py
```

## Show

stdlib heapq on the same priorities. Their empty `heappop` raises.
This kernel refuses empty tapes. See `SHOW.md`.

```bash
python3.12 show_heapq.py
```

## Evidence

Pinned `python3.12 treap_bench.py`. Numbers are copied from `results/TREAP_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `treap_root` median | 0.009842374998697778 s |
| max-priority median | 8.900000102585182e-05 s |
| root (twice) | 1306 |

## License

MIT
