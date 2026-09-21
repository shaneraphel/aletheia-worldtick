# Cuckoolock

Cuckoo-hash occupancy on a key tape. Empty keys and a failed rehash are
absence. They are not placed count 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `cuckoo.py`.

## Problems

1. **Empty key tape.** A cache or contact table with no keys must refuse.
2. **The same keys twice.** `cuckoo_placed([3,8,12], 5)` is 3 on two walks.

## Run

```bash
python3.12 cuckoolock.py --verify-precision
python3.12 cuckoo_bench.py
```

## Show

I used a stdlib dict on the same three keys. Their empty `get` is `None`.
This kernel refuses an empty key tape. See `SHOW.md`.

```bash
python3.12 show_dict.py
```

## Evidence

Pinned `python3.12 cuckoo_bench.py`. Numbers are copied from `results/CUCKOO_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n | 256 |
| n_paired | 7 |
| `cuckoo_placed` median | 0.00012216599861858413 s |
| unique median | 4.208999598631635e-06 s |
| placed (twice) | 256 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
