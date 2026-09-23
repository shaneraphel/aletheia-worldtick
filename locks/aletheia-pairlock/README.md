# Pairlock

Blossom maximum matching on a pairing graph. An empty vertex set is absence.
It is not matching size 0. Isolated vertices with `n>=1` and no edges are a
real count of 0.


## Problems

1. **Empty vertex set.** Two-hand pairing with no fingers must refuse.
2. **Isolated vertices.** `blossom_match(3, [])` is 0, a real count, not a missing graph.
3. **The same graph twice.** `blossom_match(4, [(0,1),(2,3)])` is 2 on two walks.

## Run

```bash
python3.12 pairlock.py --verify-precision
python3.12 blossom_bench.py
python3.12 show_networkx.py
```

## Show

NetworkX on the same four-finger pairing. Their empty matching is
`set()`. This kernel refuses `n<1`. See `SHOW.md`.

## Evidence

Pinned `python3.12 blossom_bench.py`. Numbers are copied from `results/BLOSSOM_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 10 |
| n_edges | 12 |
| n_paired | 7 |
| `blossom_match` median | 0.00034724999932223 s |
| greedy median | 5.420006345957518e-07 s |
| match (twice) | 4 |
| greedy match | 4 |

## License

MIT
