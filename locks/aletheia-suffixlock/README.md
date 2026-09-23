# Suffixlock

Suffix-link occupancy on a token tape. Empty text is absence. It is not
zero links.


## Problems

1. **Empty token tape.** A missing string must refuse.
2. **The same text twice.** `n_suffix_links` returns the same count on two walks.
3. **A cited tape.** Seed and n are pinned in the bench JSON.

## Run

```bash
python3.12 suffixlock.py --verify-precision
python3.12 ukkonen_bench.py
```

## Show

WojciechMula/pyahocorasick on `aba`. Their empty `add_word` is accepted.
This kernel refuses. See `SHOW.md`.

```bash
python3.12 show_ahocorasick.py
```

## Evidence

Pinned `python3.12 ukkonen_bench.py`. Numbers are copied from `results/UKKONEN_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 4096 |
| n_paired | 7 |
| `n_suffix_links` median | 0.0020482499967329204 s |
| unique-suffix set median | 0.003397541993763298 s |
| n_links (twice) | 5905 |
| n_unique_suffixes | 4096 |

## License

MIT
