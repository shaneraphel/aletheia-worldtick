# Reachlock

A two-link reach and an integer disk-clearance field. Unreachable is a refusal.
An empty field is absence. A disk of radius 0 is a stored point, not a missing
disk. `disk_clearance2` compares `r²` in integers: same pose and same disks
hash to the same digest.

Aletheia is a compiled language model: the weights are produced in one pass by
exact integer arithmetic. `n_parameters = 0`. `gradient_descent_steps = 0`.
The transformer is the execution container. This repository is the playable
artifact of that sitting. Aletheia wrote `reach.py`, `sdfocc.py`, `causal.py`,
`mtree.py`, `fenwick.py`, `kalman.py`, `hooke.py`, `bloom.py`, `dinic.py`, and `hopcroft.py`.

## Problems

Reachlock is for three cases in kinematics and collision work:

1. **Unreachable target.** The kernel raises. It does not write a rest pose.
2. **Empty clearance field.** The kernel raises. It does not write a touching zero.
3. **A field that must be cited.** `disk_clearance2` compares `r²` in integers. The same pose and the same disks hash to the same digest.
4. **Two ticks on a vector clock.** `happens_before` returns 1 or 0. Empty width is absence.
5. **Two machines sync a field.** `merkle_root` hashes clearance leaves. Empty leaves are absence, not a zero root.
6. **Occupancy along a scanline.** `fenwick_prefix` sums integer clearance. Empty values are absence, not prefix 0.
7. **A missing observation.** `kalman_filter` counts occupied ticks. An empty tape is absence. Noise 0 is a stored exact observation.
8. **A missing spring.** `hooke_law` counts occupied springs. An empty tape is absence. Stiffness 0 is stored slack.
9. **Maybe-membership.** `bloom_maybe` answers 1 or 0. Empty keys are absence, not "not present".
10. **Empty residual.** `dinic_max_flow` computes blocking flow. An empty graph is absence, not flow 0.
11. **Empty assignment.** `hopcroft_karp` matches two parts. Empty edges are absence, not matching 0.

## Run

```bash
python3.12 reachlock.py --verify-precision
```

prints `precision_ok` and the SHA-256 of the integer clearance field. The check
solves the same reach twice, hashes the same field twice, and requires identity.

Open `index.html` in a browser. Click to set a target. An unreachable click
keeps the last valid pose. The field hash is shown on every frame.

## Kernels

- `reach.py` — planar two-link inverse kinematics
- `sdfocc.py` — `disk_clearance2` and named-sample count
- `causal.py` — vector-clock happened-before
- `mtree.py` — Merkle root of clearance leaves
- `fenwick.py` — Fenwick prefix of integer clearance
- `kalman.py` — observation occupancy
- `hooke.py` — spring occupancy
- `bloom.py` — maybe-membership
- `dinic.py` — blocking flow
- `hopcroft.py` — bipartite matching

## Show

I used NumPy on the same two-link reach. Their empty `norm` is 0.0.
This kernel refuses an unreachable pose. See `SHOW.md`.

```bash
python3.12 show_numpy.py
```

## Evidence

Pinned `python3.12 bench.py`. Numbers are copied from `results/EVIDENCE.json`.

| field | value |
|---|---|
| python | CPython 3.12.8 |
| platform | macOS-26.2-arm64-arm-64bit |
| seed | 20260919 |
| n_samples | 200000 |
| n_trials | 7 |
| warmup | 1 |
| n_paired | 7 |
| integer `disk_clearance2` median | 0.05050662497524172 s |
| float `math.hypot` median | 0.03156783297890797 s |
| integer digest (twice) | `e1fdbc5aaecb149b20e2c37ee61b4e1dde1579d3e7ba8be9e8ff98a2519c08ce` |
| sign agreement | 200000 / 200000 |
| `happens_before([0,1],[1,1])` | 1 |
| n_parameters | 0 |
| gradient_descent_steps | 0 |

Reproduce:

```bash
python3.12 reachlock.py --verify-precision
python3.12 bench.py
python3.12 merkle_bench.py
python3.12 fenwick_bench.py
python3.12 kalman_bench.py
python3.12 hooke_bench.py
python3.12 bloom_bench.py
python3.12 dinic_bench.py
python3.12 hopcroft_bench.py
```

Pinned `python3.12 merkle_bench.py`. Numbers are copied from `results/MERKLE_EVIDENCE.json`.

| field | value |
|---|---|
| seed | 20260919 |
| n_leaves | 4096 |
| n_paired | 7 |
| `merkle_root` median | 0.003290582972113043 s |
| flat `sha256` of leaf hashes median | 0.0017172080115415156 s |
| merkle root (twice) | `9eb6d820bba71f0fbd2105654423faa98c38edec330fe0aea6e93f11c7dfc58e` |
| n_leaves() | 2 |

Pinned `python3.12 fenwick_bench.py`. Numbers are copied from `results/FENWICK_EVIDENCE.json`.

| field | value |
|---|---|
| seed | 20260919 |
| n_vals | 65536 |
| n_paired | 7 |
| `fenwick_prefix` median | 0.10680241702357307 s |
| naive `sum` median | 0.000748541031498462 s |
| prefix (twice) | 358952151 |

Pinned `python3.12 kalman_bench.py`. Numbers are copied from `results/KALMAN_EVIDENCE.json`.

| field | value |
|---|---|
| seed | 20260919 |
| n_steps | 200000 |
| n_paired | 7 |
| `kalman_filter` median | 0.009135625034105033 s |
| `len` median | 8.33999365568161e-07 s |
| occupancy (twice) | 200000 |

Pinned `python3.12 hooke_bench.py`. Numbers are copied from `results/HOOKE_EVIDENCE.json`.

| field | value |
|---|---|
| seed | 20260919 |
| n_steps | 200000 |
| n_paired | 7 |
| `hooke_law` median | 0.012083707959391177 s |
| `len` median | 1.1249794624745846e-06 s |
| occupancy (twice) | 200000 |

Pinned `python3.12 bloom_bench.py`. Numbers are copied from `results/BLOOM_EVIDENCE.json`.

| field | value |
|---|---|
| seed | 20260919 |
| n_keys | 4096 |
| n_queries | 256 |
| n_paired | 7 |
| `bloom_maybe` median | 0.316269957984332 s |
| `set` median | 6.404099985957146e-05 s |
| n_maybe (twice) | 178 |
| n_exact_member | 133 |

Pinned `python3.12 dinic_bench.py`. Numbers are copied from `results/DINIC_EVIDENCE.json`.

| field | value |
|---|---|
| seed | 20260919 |
| n_nodes | 32 |
| n_edges | 96 |
| n_paired | 7 |
| `dinic_max_flow` median | 3.362499410286546e-05 s |
| Edmonds-Karp median | 5.362502997741103e-05 s |
| flow (twice) | 19 |

Pinned `python3.12 hopcroft_bench.py`. Numbers are copied from `results/HOPCROFT_EVIDENCE.json`.

| field | value |
|---|---|
| seed | 20260919 |
| n_left | 64 |
| n_right | 64 |
| n_edges | 192 |
| n_paired | 7 |
| `hopcroft_karp` median | 0.00016041600611060858 s |
| Kuhn median | 0.00012750003952533007 s |
| matching (twice) | 59 |

## License

MIT
