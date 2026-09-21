# Show: I used sortedcontainers, and I refused the empty list

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [grantjenks/python-sortedcontainers](https://github.com/grantjenks/python-sortedcontainers)
on `[1,3,5,7]`: the same index 2 for key 5, plus a refusal when the list is empty.

Empty `SortedList.index` raises.
`skip_search([], 5)` raises.

```bash
python3.12 show_sortedcontainers.py
```

Pinned output: `results/SHOW_SORTEDCONTAINERS.json`.
