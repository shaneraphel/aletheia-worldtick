# Show: bitarray (the empty symbol tape)

Compared with [ilanschnell/bitarray](https://github.com/ilanschnell/bitarray) on
a five-symbol spike tape: the same rank 3 of symbol 1, plus a refusal when
the tape is empty.

bitarray 3.11.0 `count(1)` on an empty array is 0.
`wavelet_rank([], 1, 0)` raises.

```bash
python3.12 show_bitarray.py
```

Pinned output: `results/SHOW_BITARRAY.json`.
