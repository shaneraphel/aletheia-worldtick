# Show: I used Python math.gcd, and I refused a missing modulus

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with the stdlib `math.gcd` clock remainder: the same CRT 8, plus a
refusal when a modulus is missing.

`math.gcd(0, 0)` is 0. `crt_pair(2, 0, 3, 5)` raises.

```bash
python3.12 show_math.py
```

Pinned output: `results/SHOW_MATH.json`.
