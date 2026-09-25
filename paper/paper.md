# Imputation Decides

The theory in this note is about one write. An unobserved entry is replaced by a usable value, and an ordinary algorithm is then run on the completed object. The claim is that this write, not the algorithm, decides the failure. The integers below are witnesses. They are recomputed by `make evidence` and checked by `paper/check_numbers.py`.

## 1. How the statements were found

The statements were not written down and then illustrated. Three calculations refused a simpler story, and each refusal became a theorem.

**One operator, three products.** Reachability, EEG classification, and tabular action choice do not share a model. Completing the unobserved part and running the ordinary algorithm returned, in each product, the integer a fully observed input would have returned. A transition that used only an observed entry returned a different integer. The common object is the write. That is the operator split in Section 2. On the unit chain the completed reach is 3 and one measured step is 2. On the pinned world one step is 24 and the fixed point is 214.

**A scaled backup is the wrong equation.** The discount at which lookahead should leave a trap was first estimated by iterating a Bellman update on scaled integers. The action flipped too early. The update does not keep a common denominator, so its argmax is not the argmax of the true value. Replacing it by Gaussian elimination of `(I − dP)V = r` over the rationals produces `V₀ = (10 − 100d) / (1 − d²)`. Comparing a one-step deviation with that value produces the threshold `9/101`. The same algebra shows why discount 1 is excluded: the transition of the trap is a permutation, so `I − P` is singular. On the hundredths grid the action stays 0 through 0.08 and is 1 from 0.09. A depth count that treats the raw reward row as a backup reports this flip one step late. Depth 0 is the row. Depth 1 is already the infinite-horizon action on one-step traps, on all 1,000 random traps in the witness.

**“The shorter path” was too coarse.** The selection gap looked like a preference for shorter paths. Feasible-set inclusion says more, and then the gap itself split. Every cell a pessimistic planner may enter was observed free, so it is free after an optimistic fill. The pessimistic path is feasible for the optimistic planner and cannot be strictly shorter. A length score that breaks ties toward the optimistic plan therefore returns that plan on every trial where it exists. The trials in which only the pessimistic plan reaches are exactly the oracle gap. Splitting those trials by length showed that equal length is the larger part: 129 strictly shorter, 168 equal. A sentence that said only “the shorter path crashes” would have mis-counted the ties.

A fourth fact arrived with the first. After the write, the object is in the fully observed domain. A checker that looks for a mask marker has nothing to find. Its recall is 0 on maps that are still wrong.

## 2. Operators

An observation is a grid, a sample vector, or a reward table, with some entries missing.

**Optimistic imputation.** Missing map cells are written free. A dropped EEG suffix is written as zeros. The next action is the maximum of the visible reward row. An ordinary algorithm then runs: a fixed-point reachable set, a sum classifier, or one Bellman backup.

**Measured step.** Only observed entries are used. Occupied facts move across one edge. Masked grid cells are blocked. An empty EEG vector raises. The action is the optimum of one backup, not of the raw row.

**Pessimistic fill.** Missing cells are written as obstacles. Every cell the resulting path enters was observed free.

Empty input raises for each operator that would otherwise return a zero, an empty list, or a not-a-number.

## 3. Theorems

**Theorem 1 (foresight threshold).** On the reward table `[[10, 1], [-100, -100]]`, with the ring transition `(s + a + 1) mod 2`, the optimal action at state 0 flips from 0 to 1 at discount `d = 9/101`.

*Proof.* Under the stationary policy that always takes action 0, `V₀ = 10 + d V₁` and `V₁ = −100 + d V₀`, so `V₀ = (10 − 100d) / (1 − d²)` for `d ∈ [0, 1)`. A one-step deviation to action 1 in state 0 collects 1 and returns to state 0, so its action value against this continuation is `1 + d V₀`. The deviation is profitable if and only if `1 > V₀(1 − d)`. Substituting the closed form and using `1 − d² = (1 − d)(1 + d)` gives `1 > (10 − 100d) / (1 + d)`, hence `1 + d > 10 − 100d`, hence `101d > 9`. At `d = 9/101` the two action values are equal. The implementation breaks ties toward the lower action index, so the reported flip is the first grid point strictly above the threshold. ∎

**Theorem 2 (mask erasure).** Optimistic imputation emits no mask marker. Any checker that tests for a missing-data flag has recall 0 on imputed maps.

*Proof.* The fill replaces each missing entry by a free bit or by a zero. The output domain is the fully observed domain. ∎

**Theorem 3 (monotone convergence).** The set of nodes reachable in at most `h` steps from a fixed observed set, using observed edges, is nondecreasing in `h` and bounded by the least fixed point of completion, hence convergent.

**Proposition 4 (pessimistic safety).** A path that treats missing cells as blocked never enters an occluded obstacle, because every entered cell was observed free.

**Theorem 5 (breakeven).** Let `C` be the number of crashes under optimistic imputation and `W` the number of waits under the measured policy on the same corridors. The measured policy has lower total cost if and only if one crash costs more than `W/C` waits.

*Proof.* Both costs are linear in the crash price. Equality holds at `W/C`. ∎

**Theorem 6 (nested plans).** Let a cell be optimistic-feasible when it is not an observed obstacle, and pessimistic-feasible when it was observed free. The pessimistic feasible set is a subset of the optimistic one. Whenever both shortest paths exist, the optimistic path is no longer. A length score that breaks ties toward the optimistic path returns that path on every trial.

*Proof.* A pessimistic step refuses every masked cell and every observed obstacle. An optimistic step, after masked cells are written free, refuses only observed obstacles. Every pessimistic path is therefore optimistic-feasible, and a shortest optimistic path cannot be strictly longer. If the pessimistic path exists, the optimistic path exists. The tie rule then selects it. If only the optimistic path exists, the score selects it because it is the only path. ∎

Corollary. The trials where only the pessimistic plan reaches are the trials where the optimistic plan exists, does not reach, and is shorter or tied. Those trials are the oracle gap. The trials where only the optimistic plan reaches each use at least one masked cell, and that cell is truly free, because the path does not crash. Those trials are the goals a wall-fill refuses.

## 4. Comparison with cited methods

The comparison is the operator, not a shared benchmark. Robot percentages from those papers are not re-estimated.

| Work | Their method | This note | What is not claimed |
|---|---|---|---|
| [V-JEPA 2.1](https://arxiv.org/abs/2603.14482), [V-JEPA 2](https://arxiv.org/abs/2506.09985) | Predict held-out video tokens from visible context, then plan in that representation. | Do not write the missing token. One transition uses only an observed fact. The completed reach and the measured reach are different integers. | No video tokens are predicted, and no planning score on their benchmark is reported. |
| [Nilaksh, Jha, Zholus, Chandar](https://arxiv.org/abs/2605.06388) | Train latent world models and rank them once by image metrics and once by policy return. The rankings disagree. | Delete the generator. The same shortest-path routine runs on a filled map and on observed cells. The rankings still disagree: the filled integer matches the fully observed world, and the measured integer does not. | No latent is trained. Pixel fidelity is not re-measured. |
| [Yuan et al.](https://arxiv.org/abs/2609.24745) | Sample futures from a world action model. An oracle that sees realized outcomes lifts success from 68.9% to 79.2%. Selectors that score visual quality, physical consistency, or task progress recover little of that gap. | Two deterministic plans, not sampled futures. The visual score is path length on the filled map, with ties broken toward that plan. Theorem 6 says this score must return the filled plan. The witness gap is 297 reached trials, of which 129 are strictly shorter and 168 are equal length. | 68.9% and 79.2% are not re-run. |
| [Zhang, Ito, Hoshino, Ikehata, Sato](https://arxiv.org/abs/2609.02159) | Rank sampled rollouts by flow surprisal and by action-path effort, then check the chosen future against the observation that actually arrives. | There is no generator to rank. The future is one bit per masked cell. Writing that bit free or writing it blocked changes whether the path crashes. Re-observing before the step is the closed loop. | No generative surprisal is computed. |
| [LaBraM](https://arxiv.org/abs/2405.18765), InterpolatedLaBraM | Predict quantized codes of masked EEG patches. A spatial interpolation layer presents a different montage as the canonical one. | Zero-fill is the trivial form of that presentation. A filled dropout is class 0, identical to rest. The recorded window is class 1. Empty input raises. | Their tokenizer is not run. The classifier here is a sum. |

## 5. Witnesses

These counts are the checks that the statements survived contact with a pinned distribution. Seed 20260919 unless a range is named.

- Theorem 1. Discounts 0.00–0.08 select action 0. Discounts 0.09–0.95 select action 1. All 1,000 random traps flip between discount 0 and discount 0.9. The fixed trap by depth is 0, then 1.
- Theorem 2. On 10,000 corridors, filled maps still carrying a marker: 0. Filled maps matching the true corridor: 1,436. Corridors with an occluded obstacle: 8,564.
- Theorem 3. Reach by horizon: 8, 24, 50, 92, 138, 205, 212, 214. The fixed point 214 is met at 12 steps.
- Proposition 4. Pessimistic collisions: 0 on 10,000 corridors, and 0 on 2,000 grids.
- Theorem 5. One-step waits over crashes: 2,353 / 552. Full-walk waits over crashes: 20,975 / 2,995.
- Theorem 6. On 2,000 grids the inclusion holds 2,000 times and the length score matches the optimistic plan 2,000 times. Both reach 122. Only optimistic 378. Only pessimistic 297. Neither 1,203. Of the 297, 129 are strictly shorter and 168 have equal length.
- The fill, separated from the planner, on 10,000 chains: completed reach 8, measured step 2, on all 10,000. Optimistic entries into an occluded obstacle: 2,995. Measured entries: 0. Entries against mask rate 0.00–0.50: 0, 503, 934, 2002, 2914, 3970, 5,084, with the measured step at 0 throughout. EEG suffix dropout read as rest: 0, 0, 1, 9, 43, 161, 642, 2494, 10,000.

## 6. What the theory does not say

It does not say that a learned world model has the same gap on a robot benchmark. It does not say that a sum is LaBraM's tokenizer. It does not say that a tie should be broken toward the filled plan in a product. Theorem 6 says that if the product breaks ties that way, the score has already chosen the fill. A product that broke ties toward the observed-free path would keep the 168 and would still miss the 129.
