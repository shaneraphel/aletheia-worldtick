# Skiplock

Deterministic skip search on a sorted tape. An empty list is absence. A
missing key is absence. They are not index 0.


## Problems

1. **Empty list.** A lookup with no keys must refuse.
2. **A missing key.** The kernel raises. It does not write index 0.
3. **The same tape twice.** `skip_search([1,3,5,7], 5)` is 2 on two walks.

## Run

```bash
python3.12 skiplock.py --verify-precision
python3.12 skip_bench.py
```

## Show

grantjenks/python-sortedcontainers on the same tape. Their empty
`SortedList.index` raises. This kernel refuses. See `SHOW.md`.

```bash
python3.12 show_sortedcontainers.py
```

## Evidence

Pinned `python3.12 skip_bench.py`. Numbers are copied from `results/SKIP_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 65536 |
| n_paired | 7 |
| `skip_search` median | 8.417002391070127e-06 s |
| `list.index` median | 0.0007285000174306333 s |
| index (twice) | 30213 |

## License

MIT
