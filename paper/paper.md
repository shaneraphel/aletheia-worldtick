# Imputation Decides: What Filling In the Blanks Costs under Partial Observability

Worldtick technical report v1. All numbers are recomputed by `make evidence` and machine-checked by `paper/check_numbers.py` against `results/`.

## Abstract

World models, neural decoders, and action models share one inference step: impute the unobserved part of the input, then decide from the completed picture. We ask what that step costs in three minimal, fully reproducible settings — occupancy reachability, EEG classification, and tabular action selection. The findings: (1) optimistic imputation returns values identical to fully observed ones (reach 3 vs a measured step of 2; zero-filled dropout classified rest, same as true rest; myopic action 0 vs one-step-lookahead action 1); (2) on 10,000 corridors with 30% masked cells, 8,564 hide an obstacle and optimistic walking enters it 2,995 times while a measured step enters 0; (3) the same corridors decided one step at a time give 552 imputation collisions vs 0, at the price of 2,353 conservative stops; (4) pessimistic imputation (masked cells are walls) never collides and never reaches the end (0/10,000); (5) collision counts grow monotonically with the mask rate (0 to 5,084 over dropout 0.00–0.50, 70,000 corridors); (6) reach converges to its fixed point in 12 steps (8 → 24 → 50 → 92 → 138 → 205 → 212 → 214); (7) on a trap table the optimal action flips at discount exactly 9/101, proved in closed form and confirmed on 1,000 random traps (1,000/1,000 flip); (8) EEG suffix dropout reads as rest monotonically (0 → 10,000 over 0–8 dropped samples); (9) imputation deletes the mask, so a downstream missing-data checker catches 0 of 8,564 wrong maps; (10) five seeds reproduce the pattern (completion counts move, measured-side zeros never do). re-observing before every step brings collisions to 0, with 9 full traversals, 9,991 correct stops, and 20,975 waits. The fill policy, not the planner, carries the risk.

## 1. Problem

In 2026, world models, EEG foundation models, and world action models fill in what was not seen, then decide from the filled picture. V-JEPA 2.1 predicts masked video patches. Cosmos and VAE decoders reconstruct frames to high pixel fidelity. LaBraM predicts masked EEG segments; missing channels are spatially interpolated. World action models render the next observation, then select an action from the rendering.

Two 2026 studies frame the open question. Nilaksh et al. (CVPR 2026 workshop) show pixel fidelity does not imply planning performance. Zhang et al. (test-time planning, 2026) show generating plausible futures is easier than selecting the action those futures support, with oracle selection at 79.2% against 68.9% uniform and tested selectors recovering little. What has been missing is a minimal setting where both sides of that gap are exact integers. This report builds it.

## 2. Three settings

**Reachability.** A chain of cells, some observed, some masked. `world_tick` moves observed facts across one edge. `datalog_fixpoint` closes to the fixed-point reachable set. Optimistic imputation writes masked cells as free first. On 3 cells with the middle masked: imputation reaches 3, the measured step reaches 2. On the pinned world (256 nodes, 8 observed, 512 edges, seed 20260919): one step reaches 24, the fixed point is 214.

**EEG classification.** Eight samples; class is go (1) iff the sum is positive, else rest (0). The recorded trace sums positive (class 1, markers go/end). A dropped packet, zero-filled, sums to 0 (class 0), identical to true rest. Empty input raises.

**Action selection.** Trap table [[10,1],[-100,-100]] on a 2-state ring: action 0 pays more now and steps into −100; action 1 pays 1 and stays. The myopic row picks 0; one-step lookahead picks 1. On the pinned 256×8 table the myopic row picks 2 and lookahead picks 5, twice. Empty tables raise.

## 3. Theorems

**Theorem 1 (foresight threshold).** On the trap table, the optimal state-0 action flips from 0 to 1 exactly at discount d = 9/101. *Proof.* Under "always action 0", V₀ = (10−100d)/(1−d²). Q₀(a₁) = 1+dV₀ > V₀ ⟺ 1+d > 10−100d ⟺ 101d > 9. ∎ Policy evaluation solves (I−dP)V = r in exact rationals, so the threshold is sharp: discounts 0.00–0.08 give 0, 0.09–0.95 give 1.

**Theorem 2 (mask erasure).** Optimistic imputation outputs maps with zero mask markers by construction, so any downstream checker that tests for missing-data markers has recall 0 on imputed maps. Measured: 0 markers across 10,000 filled maps, of which 8,564 mismatch the true corridor.

**Theorem 3 (monotone convergence).** Single steps from the observed set form a nondecreasing reach sequence bounded by the fixed point, hence convergent; on the pinned world it meets the fixed point at 12 steps (8, 24, 50, 92, 138, 205, 212, 214) and stays flat.

**Proposition 4 (pessimistic safety).** Writing masked cells as walls never enters an occluded obstacle: every entered cell was observed free. Measured: 0 collisions in 10,000 corridors, at the price of 10,000 early stops and 0 full traversals.

## 4. Experiments

**4.1 Controlled split (10,000 trials).** Imputation vs measured step disagree everywhere: reach 8 vs 2; EEG class 0 vs 1; action 0 vs 1 — each 10,000/10,000.

**4.2 Closed-loop cost.** 32-cell corridors, 30% masked, 10,000 trials: 8,564 hide an obstacle; optimistic walking enters 2,995 times; the measured step enters 0.

**4.3 One decision.** Next-cell decisions on the same corridors: imputation collides 552 times; the measured step collides 0, with 2,353 conservative stops on free road against imputation's 0.

**4.4 Fill policy.** Optimistic: 2,995 collisions, 6,993 stops, 12 full traversals. Pessimistic: 0 collisions, 10,000 stops, 0 traversals.

**4.5 Dropout sweep.** 70,000 corridors over mask rates 0.00–0.50: imputation entries 0, 503, 934, 2002, 2914, 3970, 5084; measured step 0 throughout.

**4.6 Horizon.** Reach over horizons 0–256: 8, 24, 50, 92, 138, 205, 212, 214 at 12 steps, flat after. Per-call milliseconds grow with the horizon and flatten at the same point; on the reference machine one completion call takes ~0.09 ms.

**4.7 Foresight.** Discount grid 0.00–0.95 flips at 0.10 (theorem: 9/101 ≈ 0.089); 1,000 random trap tables flip 1,000/1,000 between d=0 and d=0.9.

**4.8 EEG dose–response.** Dropping the last k of 8 samples: rest classifications 0, 0, 1, 9, 43, 161, 642, 2494, 10000.

**4.9 Audit.** 10,000 corridors with masked cells; 0 filled maps carry markers; 1,436 match truth cell for cell; 8,564 hide an obstacle.

**4.10 Robustness.** Five seeds × 2,000 corridors: sweep entries 605, 641, 580, 606, 560; decision collisions 120, 143, 127, 126, 105; every measured-side column 0.

**4.11 Closed loop.** Re-observing the next cell before every step on 10,000 roads: 0 crashes against open-loop optimistic 2,995; 9 full traversals; 9,991 correct stops at the first observed obstacle; 20,975 waits on masked looks.

## 5. Upstream behavior

The same empty input against upstream projects: MuJoCo 3.13.0 loads an empty model; munkres 1.1.4 returns [] for compute([[]]); NumPy reports norm 0.0 and mean nan; MNE-Python reports duration 0; NetworkX reports 0 nodes; FilterPy accepts the empty update at state 0.0; MCAP/rosbag2 yield empty logs. This repository is fail-closed on each of these inputs while keeping the occupied-input values (2×2 assignment cost 2; CAKE distance 3; 8 EEG samples with go/end; 2 lidar points count 1; 3 observations count 3).

## 6. Limitations

Corridors are one-dimensional; traps are 2-state; the EEG classifier is a sum threshold. Timings are machine-specific and reported, never pinned. Robot success rates from the cited papers are not re-run; what is re-run is the shared imputation step. The claim is deliberately narrow: where the unobserved is filled optimistically, the fill decides the failure mode.

## References

- V-JEPA 2.1 (2026). https://arxiv.org/abs/2603.14482
- Nilaksh et al., Reconstruction or Semantics? CVPR 2026 workshop. https://arxiv.org/abs/2605.06388
- LaBraM (2024). https://arxiv.org/abs/2405.18765 ; InterpolatedLaBraM. https://braindecode.org/dev/generated/braindecode.models.InterpolatedLaBraM.html
- Beyond Visual Quality: test-time planning with world action models (2026). https://arxiv.org/abs/2609.24745
- World Action Planner (2026). https://arxiv.org/html/2607.27599v1
- World-Coherent Decoding (2026). https://arxiv.org/abs/2609.02159
