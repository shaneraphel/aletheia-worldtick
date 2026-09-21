# Needlelock

Aho–Corasick hit count on a token tape. Empty text is absence. An empty
pattern is absence. They are not hit count 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `acauto.py`.

## Problems

1. **Empty text.** A world-model or event detector with no tape must refuse.
2. **An empty pattern.** A missing needle is absence, not "no hits".
3. **The same tape twice.** `aho_hits("abcabc", ["ab","bc"])` is 4 on two walks.

## Run

```bash
python3.12 needlelock.py --verify-precision
python3.12 acauto_bench.py
python3.12 show_ahocorasick.py
```

## Show

I used pyahocorasick on the same tape. Empty `add_word` is accepted there.
This kernel refuses. See `SHOW.md`.

## Evidence

Pinned `python3.12 acauto_bench.py`. Numbers are copied from `results/AHO_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 65536 |
| n_paired | 7 |
| `aho_hits` median | 0.005757541999628302 s |
| start-scan median | 0.020306750000600005 s |
| hits (twice) | 29138 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
