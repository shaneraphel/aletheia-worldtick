# Remainlock

Two-modulus Chinese remainder. A non-positive modulus is absence. Non-coprime
moduli are absence. They are not residue 0.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `crt.py`.

## Problems

1. **A missing modulus.** Sensor-fusion or clock remainders with `m<=0` must refuse.
2. **Non-coprime moduli.** The kernel raises. It does not write a false residue.
3. **The same pair twice.** `crt_pair(2,3,3,5)` is 8 on two walks.

## Run

```bash
python3.12 remainlock.py --verify-precision
python3.12 crt_bench.py
python3.12 show_math.py
```

## Show

I used `math.gcd` on the same clock pair. Their `gcd(0, 0)` is 0. This
kernel refuses a missing modulus. See `SHOW.md`.

## Evidence

Pinned `python3.12 crt_bench.py`. Numbers are copied from `results/CRT_EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_pairs | 2000 |
| n_paired | 7 |
| `crt_pair` median | 0.002904041961301118 s |
| brute median | 0.003883084049448371 s |
| xor (twice) | 80 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

## License

MIT
