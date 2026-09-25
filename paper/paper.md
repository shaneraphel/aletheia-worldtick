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

**Theorem 7 (a tie cannot be an optimistic-only success).** Assume the nested feasible sets of Theorem 6, and assume a pessimistic path never enters an obstacle. If the two shortest paths have equal length, both exist, and the pessimistic plan reaches. Therefore no equal-length trial is a success of the optimistic plan alone.

*Proof.* Equal length is only defined when both paths exist. A pessimistic path enters only cells observed free, so it reaches. The trial is then either a success of both plans, or a success of the pessimistic plan alone. It is not a success of the optimistic plan alone, because that case has no pessimistic path, hence no length to tie. ∎

Switching the tie from the filled plan to the observed-free plan therefore turns each equal-length gap trial from a crash into a reach, and it does not remove any optimistic-only success. On the pinned grids the equal-length gap is 168 and the optimistic-only count is 378, with zero ties among them. The strict shortenings are a different set: 185 trials, of which 56 still reach and 129 are the rest of the gap. A shorter path is not a certificate of safety, and it is not a certificate of failure.

This split was forced by asking whether the 168 ties were a harmless convention. Inclusion says they are not. A tie means the observed-free path exists and arrives. The convention that breaks the tie toward the filled plan is the whole reason those 168 goals are missed. No change of tie rule reaches the 129, because on those trials the filled path really is shorter, and it is shorter by using a masked cell.

**Theorem 8 (zero is not the identity of the decision).** Let the class be 1 when the sum of the samples is positive, and 0 otherwise. Replacing a set of coordinates by zero changes the sum by the negative of the erased coordinates. If every sample is non-negative, the class cannot rise. If some sample is negative, the class can rise.

*Proof.* The filled sum equals the original sum minus the erased sum. A non-negative erased sum cannot increase the total, so a non-positive original sum stays non-positive. A negative erased coordinate can lift a non-positive sum above zero. The packet `[1, 0, 0, 0, 0, 0, 0, -2]` has sum −1 and class 0. Zeroing the last sample leaves sum 1 and class 1. ∎

The dose curve that only falls toward rest was produced by a generator that draws samples from `{0, 1, 2, 3}`. On that generator a false go is impossible, and the witness is identically zero at every suffix length. The same write on samples from `{-2, -1, 0, 1, 2}` produces both errors. Dropping the last 4 of 8 samples: 1280 packets that were a movement are read as rest, and 1141 packets that were rest are read as a movement. A product that zero-fills a dropout is not choosing the conservative error. The direction of the error is the sign of what it deleted. The old sweep could not show the second direction, because its generator had no negative samples.

**Theorem 9 (one answer does not finish the repair).** Suppose the optimistic path crashes, and let `c` be the first obstacle on that path. Then `c` was masked. Blocking `c` and planning again on the same filled map does not restore safety. The remaining masked cells are still written free, so the new path can crash on a later one.

*Proof.* An optimistic path enters a true obstacle only where the observation was missing; an observed obstacle is blocked before the search. So `c` is masked. Blocking `c` removes one feasible cell. It does not change the fill of any other masked cell. A path that uses one of those cells, if that cell is an obstacle, crashes. ∎

The closed loop is the operator that matches the proof: observe again before the next step, rather than asking once and trusting the rest of the fill. On the 2,000 grids the optimistic plan crashes 1,439 times, and the first crash cell is masked all 1,439 times. After blocking that cell, 614 paths reach, 786 crash on a later cell, and 39 have no path. One question repairs fewer crashes than it leaves behind.

This was forced by asking whether the closed loop was wasteful. If the first collision were the only collision, one question would be the product and the thousands of waits would be the wrong design. They are not. The fill of the cells we did not ask about is still a decision.

**Theorem 10 (the filled plan can hide more than one obstacle).** Repeat the step in Theorem 9: while the path crashes, block its first obstacle and plan again. Each question blocks a cell that was not blocked before, and the grid is finite, so the process ends at a path that arrives or at no path. It does not end at one question.

*Proof of termination.* An observed obstacle is blocked from the start. A newly blocked cell is a masked obstacle, hence not yet in the blocked set. The set grows by one cell each question and cannot grow past the number of cells. ∎

On the 2,000 grids the process never hits the cap. 561 grids need no question. 653 need exactly one. 786 need more than one. The histogram of questions is 561, 653, 422, 217, 90, 41, 13, 2, then one grid at 9, and none at 8. The questions total 2814. Asking until the path is clear ends at 1854 arrivals and 146 stops. The 786 is not a thin tail. It is the majority of the grids that crash.

**Theorem 11 (a scene change on a filled window is a class error).** Let a window be incomplete when a suffix was not observed. Zero-filling that suffix and then changing the sound or the picture according to the filled class changes the scene if and only if the filled class differs from the class of the recorded samples. Holding the scene whenever the suffix is missing makes that count zero.

*Proof.* The filled class differs from the recorded class exactly on a false rest or a false go, which is Theorem 8. A hold does not consult the filled class. ∎

On 10,000 signed windows with the last 4 samples dropped, the filled class would retune 2421 windows: 1280 false rests and 1141 false gos. The hold count is 10,000. On the 2,000 hand maps, rendering the filled grasp crosses an obstacle 1,439 times. Refusing to draw that completion crosses it 0 times. Neither number is a clinical effect. Both are the same write, applied once to a brain window and once to a camera.

The same refusal applies to the file the picture and the sound are stored in. Python's `wave` module writes a legal file with 0 frames. SciPy 1.17.1 and soundfile 0.14.0 read that emptiness back as a length-0 array at 8,000 Hz. Pillow 11.3.0 constructs a 0×0 RGB image. OpenCV 5.0.0 counts 0 nonzero pixels in an empty image. Open3D 0.20.0 returns a cloud with 0 points and a mesh with 0 vertices. An 8-sample tone is class 1 and is 8 frames. Empty samples raise. Splitting the 2,000 hand maps across 10 cores does not change the crash count: serial and parallel are both 1,439.

**The rate already playing.** A complete window may set the left-right rate: 2 clicks a second when the recorded sum is not positive, 6 when it is. An incomplete window keeps whatever rate is already playing. On 10,000 steps, seed 20260919, a window is dropped with probability 0.30, which happened 3057 times. On those dropped steps a zero-fill would have chosen the other rate 712 times. The rate already playing changed 0 times. On complete windows the rate is allowed to follow the recording, and it did so on 3379 steps. This is not a reading of fright. It is the condition under which the sound may change.

**The picture stops at the camera.** The hand is drawn only on cells that were observed free. On the same 2,000 maps the drawn part is 6657 cells and contains 0 obstacles. The filled path continues for another 53456 cells, of which 2474 are real obstacles. On 1938 maps the filled picture would have drawn past the last cell the camera saw. Ten cores and one core agree. The other people in the room are not on this path. They stand still. The picture does not turn them into a route, and it does not walk the hand through a cell the camera did not see.

**An attempt is not a step.** A complete window with a positive sum may set the rate to 6. If the next cell was not seen, the picture stays. On 2,000 maps paired with 2,000 windows (map seed 20260919, window seed 20260920), that pair happens 630 times. The window was dropped on 572 maps, and then both the rate and the picture hold. A movement with a seen next cell happens 22 times: only then may the picture step. The remaining 776 complete windows are not movements. Ten cores agree. A fill would have drawn the 630 unseen steps as grasps. The coach does not. This is not an emotion. Both facts were observed.

**The record.** Each map is one row. A dropped window stores no class. The hand's cell is the last cell observed free. On these 2,000 rows, classes stored are 1428, which is every complete window and none of the dropped ones. A class written on a drop is 0. A hand cell that was not seen is 0. The 630 refused steps are stored as refused, not as grasps. Ten cores write the same counts. This is not data taken from a person. It is the shape the record is allowed to have, for the hand practice and for the sound that stayed.

**Who is in the room.** Two people stand on the same cells of every map, (4, 4) and (8, 8). They do not move, and the hand is not sent to them. A person is drawn only when that cell was seen. Across 4,000 person-cells, 3003 were seen and 997 were not, so those 997 are absent from the picture. The filled path walks through an unseen person 19 times. The path that stays on seen cells walks through a seen person 2 times. The extra crossings exist because a missing cell was written free. Ten cores agree with one.

**The next frame.** Paint only the cells that were seen, and put the hand on the last of those that were free. Paint that frame a second time, with no new observation: on all 2,000 maps the pixels match, so the repaint count is 0. Paint the missing cells as well: the frame differs on all 2,000 maps, and 127697 unseen cells receive a color. The picture changed because the fill wrote into cells the camera did not see. One core and ten cores agree.

**One clock.** Sixteen windows arrive on each of the 2,000 maps. A dropped window changes neither the rate nor the frame: both of those counts are 0. The picture steps 3665 times, only when the window is a movement and a seen cell remains. The rate, which may follow a complete window even after that, changes 10933 times. After the seen cells are used up, a movement is still heard 6414 times and the picture does not step. The sound outlasts the camera. Ten cores agree.

## 4. Comparison with cited methods

The comparison is the operator, not a shared benchmark. Robot percentages from those papers are not re-estimated.

| Work | Their method | This note | What is not claimed |
|---|---|---|---|
| [V-JEPA 2.1](https://arxiv.org/abs/2603.14482), [V-JEPA 2](https://arxiv.org/abs/2506.09985) | Predict held-out video tokens from visible context, then plan in that representation. | Do not write the missing token. One transition uses only an observed fact. The completed reach and the measured reach are different integers. | No video tokens are predicted, and no planning score on their benchmark is reported. |
| [Nilaksh, Jha, Zholus, Chandar](https://arxiv.org/abs/2605.06388) | Train latent world models and rank them once by image metrics and once by policy return. The rankings disagree. | Delete the generator. The same shortest-path routine runs on a filled map and on observed cells. The rankings still disagree: the filled integer matches the fully observed world, and the measured integer does not. | No latent is trained. Pixel fidelity is not re-measured. |
| [Yuan et al.](https://arxiv.org/abs/2609.24745) | Sample futures from a world action model. An oracle that sees realized outcomes lifts success from 68.9% to 79.2%. Selectors that score visual quality, physical consistency, or task progress recover little of that gap. | Two deterministic plans, not sampled futures. The visual score is path length on the filled map, with ties broken toward that plan. Theorem 6 says this score must return the filled plan. The witness gap is 297 reached trials, of which 129 are strictly shorter and 168 are equal length. | 68.9% and 79.2% are not re-run. |
| [Zhang, Ito, Hoshino, Ikehata, Sato](https://arxiv.org/abs/2609.02159) | Rank sampled rollouts by flow surprisal and by action-path effort, then check the chosen future against the observation that actually arrives. | There is no generator to rank. The future is one bit per masked cell. Writing that bit free or writing it blocked changes whether the path crashes. Re-observing before the step is the closed loop. | No generative surprisal is computed. |
| [LaBraM](https://arxiv.org/abs/2405.18765), InterpolatedLaBraM | Predict quantized codes of masked EEG patches. A spatial interpolation layer presents a different montage as the canonical one. | Zero-fill is that presentation with the code replaced by zero. On a non-negative code the class can only fall to rest. On a signed voltage the same write can raise a rest to a movement, because the erased sum can be negative. Empty input raises. | Their tokenizer is not run. The classifier here is a sum. The non-negative dose curve is the special case, not the general one. |

## 5. Witnesses

These counts are the checks that the statements survived contact with a pinned distribution. Seed 20260919 unless a range is named.

- Theorem 1. Discounts 0.00–0.08 select action 0. Discounts 0.09–0.95 select action 1. All 1,000 random traps flip between discount 0 and discount 0.9. The fixed trap by depth is 0, then 1.
- Theorem 2. On 10,000 corridors, filled maps still carrying a marker: 0. Filled maps matching the true corridor: 1,436. Corridors with an occluded obstacle: 8,564.
- Theorem 3. Reach by horizon: 8, 24, 50, 92, 138, 205, 212, 214. The fixed point 214 is met at 12 steps.
- Proposition 4. Pessimistic collisions: 0 on 10,000 corridors, and 0 on 2,000 grids.
- Theorem 5. One-step waits over crashes: 2,353 / 552. Full-walk waits over crashes: 20,975 / 2,995.
- Theorem 6. On 2,000 grids the inclusion holds 2,000 times and the length score matches the optimistic plan 2,000 times. Both reach 122. Only optimistic 378. Only pessimistic 297. Neither 1,203. Of the 297, 129 are strictly shorter and 168 have equal length.
- Theorem 7. Equal-length optimistic-only successes: 0. Strict shortenings that still reach: 56. Those 56 plus the 129 shorter gap trials are the 185 strict shortenings.
- Theorem 8. Non-negative false go, every suffix: 0. Signed packets, last 4 samples zeroed: false rest 1280, false go 1141.
- Theorem 9. Optimistic crashes on 2,000 grids: 1,439, and the first crash cell was masked in all 1,439. After blocking that one cell: 614 reach, 786 crash again, 39 stop.
- Theorem 10. Questions until the path is clear, over 2,000 grids: 561, 653, 422, 217, 90, 41, 13, 2, and one grid at 9. More than one question: 786. Questions total: 2814. The process ends at 1854 arrivals and 146 stops.
- Theorem 11. Signed windows, last 4 samples zero-filled: the scene would retune on 2421 of 10,000, and the hold retunes 0. Filled grasp pictures cross an obstacle 1,439 times on 2,000 maps. The coach draws that completion 0 times.
- The fill, separated from the planner, on 10,000 chains: completed reach 8, measured step 2, on all 10,000. Optimistic entries into an occluded obstacle: 2,995. Measured entries: 0. Entries against mask rate 0.00–0.50: 0, 503, 934, 2002, 2914, 3970, 5,084, with the measured step at 0 throughout. EEG suffix dropout read as rest: 0, 0, 1, 9, 43, 161, 642, 2494, 10,000.

## 6. What the theory does not say

It does not say that a learned world model has the same gap on a robot benchmark. It does not say that a sum is LaBraM's tokenizer. It does not say that a tie should be broken toward the filled plan in a product. Theorem 6 says that if the product breaks ties that way, the score has already chosen the fill. Theorem 7 says that breaking them the other way keeps the 168 and loses none of the 378, and still misses the 129. Theorem 8 says that a zero-fill which only hides movement is an artifact of non-negative samples. Theorem 9 says that asking about the first crash and then trusting the rest of the fill leaves 786 crashes in place.
