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

**Nearby is not seen ground.** From the last cell the camera saw to be free, walk to a person at (4, 4) or (8, 8). On seen ground the walk enters only cells observed free. On the filled map a missing cell counts as free. Across these maps the filled walk reaches a person the seen walk cannot reach 2301 times. When both walks arrive, the filled walk is strictly shorter 560 times, out of 1192 arrivals by both. The people do not move, and the hand is not sent to them. The shorter number is what the filled picture would call nearby. Ten cores agree.

**Sound without a new frame.** The frame is the seen map and the hand cell. It does not contain the rate. On the same clocks, the pixels change 3665 times, which is exactly the number of picture steps. The rate changes while the picture stays 8377 times. A dropped window changes the pixels 0 times. The sound is allowed to follow a complete window. The picture is not required to redraw when it does. Ten cores agree.

**Theorem 12 (a missing joint sample is not a closure).** Let a finger code lie in {0, …, 7}, and let 0 mean closed. A sample is either missing or a code. The coach state is the last code received, or absent when none has been received. The coach draws the finger closed only when that state is 0. The zero buffer draws it closed when the sample is missing or the sample is 0. Then every coach closure is also a buffer closure. Every extra buffer closure is a missing sample whose coach state is not 0: either no sample has arrived, or the last received code was open.

*Proof.* If the sample is a code, both states become that code, so they agree. If the sample is missing, the buffer draws closed and the coach state is unchanged. The coach then draws closed only when the unchanged state is already 0, which means a 0 was received earlier. An absent state is not 0, so a finger with no sample yet is not drawn closed by the coach. A buffer of five codes allocated as zeros is five closures before any sample; the coach, given no sample, does not draw them. ∎

On 2,000 hands, sixteen packets, and five fingers, that is 160000 finger-steps, seed 20260919. The buffer draws a closure the coach does not draw on 43014 steps. Of those, 38623 had last been seen open, and 4391 had never arrived. The coach draws 19335 closures, and the buffer draws all 19335 of them. A coach closure with no received 0 happens 0 times. A fresh `bytearray` of length 5 reads `[0, 0, 0, 0, 0]`. Ten cores agree. This is not a recording from a hand. It is the picture a zero write produces.

**Theorem 13 (a late signal is not a default).** At each step a brain stretch and a finger angle either arrive or are missing, independently, with missing probability 0.30. The held picture updates the sound only when the stretch arrived, and updates the finger only when the angle arrived. Before the first arrival the sound stays slow and the finger is not drawn closed. The guessed picture reads a missing stretch as rest and draws a missing finger closed. Whenever both arrived, the two pictures are the same, because both adopt the values that arrived. They differ only when a missing part is replaced by a default the held picture is not already showing.

*Proof.* If a part arrived, both pictures set it to that value. If it is missing, the guessed picture writes the default and the held picture keeps its previous value. Equality fails exactly when the default and the previous value disagree. A step on which both parts arrived therefore cannot be a disagreement. ∎

On 10,000 sessions of 16 steps, 160000 steps in all, seed 20260919, the pictures differ on 58569 steps. The sound differs on 21864 of them and the finger on 42417. On the steps where both signals arrived, the pictures differ 0 times. One core and ten cores agree. These are not recordings from a person. A real-time frame still has to be shown; the held picture shows the last values that arrived, and the guessed picture shows a default for whatever is late.

**Theorem 14 (tenants do not move each other).** A service holds one picture per tenant: the last sound and the last finger that tenant sent. A request updates only the held picture of the tenant that sent it. Then the sequence a tenant sees is a function of that tenant's own requests alone. Grouped service, round-robin service, and service with an added tenant that sends nothing all show each tenant the same sequence.

*Proof.* The held picture of tenant t is written only by requests carrying t. Its value before t's k-th request is therefore determined by t's first k-1 requests. The picture shown for that request is this held value updated by the arrivals in the request itself. No request from another tenant appears in either step. ∎

On 16 tenants with 500 requests each, 8000 requests in all, seed 20260919, all 16 tenants see identical sequences under grouped and round-robin service. Adding a tenant that sends nothing leaves all 16 unchanged. The guess and the held picture differ on 2981 requests. Requests with something late are 4078. Requests where both arrived are 3922. One core and ten cores agree. These are not requests from people.

**Theorem 15 (the picture knows how old it is).** Each part of the held picture carries an age: 0 when that stream arrived this step, one more than before when it did not. The frame age is the older of the two parts. A three-step burst with both streams missing raises both ages by exactly 3 and leaves the held picture unchanged. The guessed picture shows a default for whatever is late and presents it as new.

*Proof.* Ages update by the stated rule, so each part's age is the steps since its stream last arrived. Held values are written only on arrival. During the burst there is no arrival, so after each of the three steps the held picture equals the picture before the burst, while both ages have grown by 1. ∎

On 10,000 sessions of 16 steps with steps 6, 7, and 8 missing both streams, 160000 steps in all, seed 20260919, frames where both arrived this step are 63903. Frame ages summed over every step are 199886. The oldest frame is 12. The guess and the held picture differ on 75353 steps. Burst steps with the held picture unchanged are 30000. Sessions reaching age 5 are 3939. One core and ten cores agree. These are not recordings from a person.

**Theorem 16 (being right by luck is not a measurement).** Every step draws true values independently of arrivals: the brain is a movement with probability 1/2, and the finger is uniform on eight codes with 0 closed. On a step where the brain stretch is missing, the default rest matches the truth with probability 1/2. Where the finger angle is missing, the default closed matches with probability 1/8. Where both are missing, both defaults match with probability 1/16. The held picture keeps the last arrival and starts open, so on finger-late steps it matches with probability 1/8 after the first arrival and 7/8 before it.

*Proof.* True values are drawn independently of the missing pattern, so P(true rest) = 1/2, P(true closed) = 1/8, and the joint match is the product 1/16. A held finger that arrived before shows its last code, uniform and independent of the current truth, matching with probability 1/8. Before the first arrival it shows open, matching with probability 7/8. ∎

On 10,000 sessions of 16 steps, 160000 steps, seed 20260919, steps with something late are 81428. The guess matches the truth on 21801 of them. The held picture matches on 48700. Brain-only-late steps are 33484: the guess matches 16776, the held picture 16554. Finger-only-late steps are 33670: the guess matches 4150, the held picture 26544. Both-late steps are 14274: the guess matches 875, the held picture 5602. The missing brain stretch is truly rest 23856 times out of 47758. The missing finger is truly closed 5978 times out of 47944. One core and ten cores agree. These are not recordings from a person.

**Theorem 17 (the picture catches up on the first full arrival).** After a burst, the held picture equals the truth from the first step on which both streams arrive, because each arrival adopts the true value. Steps between the burst and that step show earlier values for whatever is still late.

*Proof.* On a step where both streams arrive, both held parts are set to the true values of that step. Before the first such step after the burst, at least one part still shows a value from an earlier step. ∎

On 10,000 sessions of 16 steps with steps 6, 7, and 8 missing, seed 20260919, delays to the first full arrival after the burst are 4938, 2531, 1230, 646, 311, 180, 77, and 87 sessions never see one in the remaining seven steps. The delays sum to 19448. On the 10144 steps before the catch-up step, the held picture matches the truth 6022 times and the guess 2693. Steps where the catch-up picture differs from the truth: 0. One core and ten cores agree. These are not recordings from a person.

**Theorem 18 (streams that were never the same speed).** The brain stretch arrives every step unless it drops. The finger angle arrives every third step and never in between. Then the frame is new only on a scheduled step whose stretch also arrived: at most 6 of 16 steps in a session, even if the brain never drops. The finger age cycles 0, 1, 2 no matter what the brain does, summing to exactly 15 per session. The guess treats all sixteen steps as new.

*Proof.* A frame needs both parts from this step. The finger has this step's angle only on the 6 scheduled steps, so no session can show more than 6 new frames. On step t the finger age is t mod 3 by the schedule, and 0 + 1 + 2 repeated over steps 0 to 14 plus step 15 sums to 15. ∎

On 10,000 sessions of 16 steps, 160000 steps, seed 20260919, fully new frames are 42145. Finger ages sum to exactly 150000. Missing brain stretches are 47865. Steps where the guess and the held picture differ are 96605. One core and ten cores agree. These are not recordings from a person.

**Theorem 19 (two hands in one room move independently).** Two players share one frame. Each hand updates only on its own arrivals. Serving A's request before B's, or B's before A's, shows both players the same pair of hands, because the two updates touch disjoint states. A player whose streams both miss leaves the other player's hand exactly as that player's own arrivals dictate.

*Proof.* Each update reads and writes one player's held values only. The two players' states are disjoint, so the order of the two writes cannot change either result. A fully missing player contributes no write, and the other player's hand follows its own arrivals alone. ∎

On 10,000 pairs of 16 steps, 160000 steps, seed 20260919, steps where both hands moved are 132416. Only A moved on 13146 steps, only B on 13117, and neither on 1321. A fully dark A with B moving is the same 13117 steps, and a fully dark B with A moving is the same 13146. Steps changed by serving order: 0. One core and ten cores agree. These are not recordings from people.

**Theorem 20 (fewer arrivals, fewer new frames).** Six rates threshold the same uniforms: 0.00, 0.10, 0.20, 0.30, 0.40, 0.50. Both streams arrive exactly when both uniforms clear the rate, so the new-frame share is (1-p)^2 in expectation, and a higher rate misses a superset of a lower rate's misses. With nothing late the two pictures never differ, because every step both arrive and both adopt the same values.

*Proof.* Arrival of each stream is its uniform clearing p, independently, so P(both arrive) = (1-p)^2. At p = 0 every uniform clears. Nesting holds because a uniform below the lower threshold is below the higher one. ∎

On 10,000 sessions of 16 steps, 160000 steps, seed 20260919, new frames across the six rates are 160000, 129652, 102479, 78572, 57683, 40037. Steps where the guess and the held picture differ are 0, 20843, 40359, 58471, 75109, 90720. One core and ten cores agree. These are not recordings from a person.

**Theorem 21 (the oldest a frame can get on a miss budget).** Sixteen steps, and each stream may miss k of them. No frame is older than k steps, and missing the last k steps reaches k. The frame ages then sum to k(k+1)/2 per session, and new frames are 16-k per session.

*Proof.* An age counts the misses since the last arrival, so no age exceeds the miss budget. Missing the last k steps grows the ages 1 through k, reaching k with the triangular sum. ∎

On 10,000 sessions, seed 20260919, oldest frames for budgets 0 to 8 are 0 through 8. Age sums are 0, 10000, 30000, 60000, 100000, 150000, 210000, 280000, 360000. New frames are 160000 down to 80000 in steps of 10000. Steps where the guess and the held picture differ are 0, 9346, 18750, 27972, 37700, 46715, 56436, 65436, 75184. One core and ten cores agree. These are not recordings from a person.

**Theorem 22 (the record replays itself).** Every step logs its arrivals. The shown picture is a pure function of those rows: one replay walks forward updating held values, and another recomputes each step from scratch by scanning all rows from the session start. Both show the online picture on every step.

*Proof.* The held update is deterministic given the arrivals. By induction over the steps, the forward walk holds the online values after each row. The rescan applies the same transition to the same prefix, so it holds the same values at each step. ∎

On 10,000 sessions of 16 steps, 160000 rows, seed 20260919, replayed steps are 160000 and steps where the three pictures differ are 0. Sessions matching on every step are all 10000. Held values changed on 71442 steps. New frames are 78861. Steps where the guess differs are 58450. One core and ten cores agree. These are not recordings from a person.

**Theorem 23 (each stream multiplies the new-frame share).** Three streams arrive independently at rate 0.7. All three arrive with probability 0.7^3, and none arrive with probability 0.3^3. Adding the third stream multiplies the two-stream new-frame share by 0.7.

*Proof.* Arrivals are independent across streams, so P(all three arrive) = 0.7^3 and P(none arrive) = 0.3^3. The two-stream share 0.7^2 times the third stream's 0.7 is 0.7^3. ∎

On 10,000 sessions of 16 steps, 160000 steps, seed 20260919, steps where all three arrived are 55321. Steps where the guess and the held picture differ are 85303. Steps where nothing arrived are 4306. One core and ten cores agree. These are not recordings from a person.

**One batch, two processors.** One hundred thousand sessions run once on the CPU and once on the Mac GPU, counting from the same integer uniforms against the threshold 1288490188. The CPU reference is one Python process. The GPU runs one thread per session under Metal. Both count 783232 new frames and 586904 disagreements, matching elementwise on all 100000 sessions. The GPU is an Apple M4 part. This is a platform witness: the same batch, the same answer, another chip. It is not a claim about speed.

**The clearing.** Four models from Kenney's Nature Kit, 205 vertices and 478 triangles, stand in fixed places. Over sixteen steps the hand the user sees advances on 6 arrivals and stops at place 6. The guessed picture advances on every step and stops at place 16. Replaying the record mismatches 0 times. The models are CC0. This is not a shipped game level.

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
- Theorem 12. On 160,000 finger-steps the zero buffer draws 43014 closures the coach does not. 38623 of them were last seen open. 4391 had never arrived. Coach closures are 19335, and all of them are buffer closures. Coach closures with no received 0: 0.
- Theorem 13. On 160,000 steps the guessed picture and the held picture differ 58569 times: the sound on 21864, the finger on 42417. When both signals arrived they differ 0 times.
- Theorem 14. On 8000 requests from 16 tenants, grouped and round-robin service show each tenant the same sequence, 16 of 16. A silent added tenant leaves all 16 unchanged. The guess differs on 2981 requests. Late requests are 4078. Full arrivals are 3922.
- Theorem 15. On 160000 steps with a 3-step burst, new frames are 63903, ages sum to 199886, the oldest frame is 12, the guess differs on 75353 steps, and the held picture is unchanged on all 30000 burst steps.
- Theorem 16. On 81428 late steps the guess matches 21801 times and the held picture 48700. Brain-only: 16776 against 16554. Finger-only: 4150 against 26544. Both-late: 875 against 5602.
- Theorem 17. Delays after the burst: 4938, 2531, 1230, 646, 311, 180, 77, and 87 never. Delays sum to 19448. Before the catch-up step the held picture matches 6022 times and the guess 2693. Catch-up mismatches: 0.
- Theorem 18. With the finger scheduled every third step, new frames are 42145, finger ages sum to exactly 150000, missing stretches are 47865, and the guess differs on 96605 steps.
- Theorem 19. On 160000 shared steps both hands moved 132416 times, only A 13146, only B 13117, neither 1321. Serving order changed 0 steps.
- Theorem 20. Across rates 0.00 to 0.50, new frames are 160000, 129652, 102479, 78572, 57683, 40037, and disagreement is 0, 20843, 40359, 58471, 75109, 90720.
- Theorem 21. On budgets 0 to 8 the oldest frames are 0 through 8, age sums are triangular to 360000, and disagreement is 0, 9346, 18750, 27972, 37700, 46715, 56436, 65436, 75184.
- Theorem 22. On 160000 rows both replays match the online picture on every step: mismatches 0, clean sessions 10000. Held changed 71442 times. New frames 78861. Guess differs 58450.
- Theorem 23. On 160000 steps with three streams, all three arrived 55321 times, nothing arrived 4306 times, and the guess differs 85303 times.
- Two processors. On 100000 sessions the CPU and the GPU count 783232 new frames and 586904 disagreements, mismatching on 0 sessions.
- The fill, separated from the planner, on 10,000 chains: completed reach 8, measured step 2, on all 10,000. Optimistic entries into an occluded obstacle: 2,995. Measured entries: 0. Entries against mask rate 0.00–0.50: 0, 503, 934, 2002, 2914, 3970, 5,084, with the measured step at 0 throughout. EEG suffix dropout read as rest: 0, 0, 1, 9, 43, 161, 642, 2494, 10,000.

## 6. What the theory does not say

It does not say that a learned world model has the same gap on a robot benchmark. It does not say that a sum is LaBraM's tokenizer. It does not say that a tie should be broken toward the filled plan in a product. Theorem 6 says that if the product breaks ties that way, the score has already chosen the fill. Theorem 7 says that breaking them the other way keeps the 168 and loses none of the 378, and still misses the 129. Theorem 8 says that a zero-fill which only hides movement is an artifact of non-negative samples. Theorem 9 says that asking about the first crash and then trusting the rest of the fill leaves 786 crashes in place. Theorem 12 says that storing a missing joint sample as zero draws a closure. It does not say that a prosthesis sent those angles. Theorem 13 says that a real-time frame which writes a default for a late signal shows a different picture from the last one that actually arrived. It does not say the default was a reading of fright, or of a hand. Theorem 14 says that a service which keys its held picture by tenant cannot let one tenant's dropout move another tenant's picture. It does not say such a service is already running. Theorem 15 says that a held picture can report how many steps old each part is. It does not say that an old frame is safe to act on. Theorem 16 says that a default is right with probability 1/2, 1/8, or 1/16, and that keeping the last arrival beats the default on finger-late steps. It does not say that matching the truth by luck is a measurement. A lucky match is still luck. Theorem 17 says the picture matches the truth from the first full arrival after a burst. It does not say the wait is short, or that matching once means staying matched. Theorem 18 says that streams on different schedules make most frames old by construction. It does not say the schedules cannot change, only what this one costs. Theorem 19 says that two hands sharing one frame move independently. It does not say the two players see each other, only that neither player's misses move the other's hand. Theorem 20 says that fewer arrivals mean fewer new frames and more disagreement. It does not say which rate a product will see. Theorem 21 says that a miss budget bounds every frame age and the bound is tight. It does not say misses arrive in the worst order. Theorem 22 says that the arrival record replays the shown pictures exactly. It does not say the record cannot be lost, only that keeping it is enough. Theorem 23 says that each added stream multiplies the new-frame share by its arrival rate. It does not say streams arrive independently in a product. The GPU run says the same integers give the same counts on another chip. It does not say the GPU is faster.
