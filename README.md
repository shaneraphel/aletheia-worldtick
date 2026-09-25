# Worldtick

[![check](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml/badge.svg)](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml)

A boundary in front of a world model, a neural decoder, or a planner. Cells that were not observed stay unobserved. Empty input is refused, and does not come back as zero.

放在世界模型、神经解码器或规划器前面的一道边界。没观测到的格子保持没观测到。空输入被拒绝，不会变成 0。

## Where shipped products get stuck

Three products share one stuck step. The model or the map is asked to return a complete scene, and the next module treats that scene as measured.

**World models.** [Cosmos](https://github.com/nvidia-cosmos/cosmos-predict1) and [V-JEPA 2.1](https://arxiv.org/abs/2603.14482) are used as “imagine the next frame, then act.” The frame that leaves the model has no holes. [Nilaksh et al.](https://arxiv.org/abs/2605.06388) showed that a latent can win on pixels and lose on the plan. [Yuan et al.](https://arxiv.org/abs/2609.24745) showed that an oracle, which sees the real outcome of each imagined future, lifts success from 68.9% to 79.2%, while selectors that score the picture recover little of that gap. The product difficulty is not drawing the future. It is that the drawn future no longer says which part was guessed. [Zhang et al.](https://arxiv.org/abs/2609.02159) make the same point from the other side: which future you keep changes the action.

**Brain–computer interfaces.** [LaBraM](https://arxiv.org/abs/2405.18765) predicts masked EEG, and [InterpolatedLaBraM](https://braindecode.org/dev/generated/braindecode.models.InterpolatedLaBraM.html) exists so a checkpoint always sees its training montage. A dropped packet written as zeros is classified as rest, the same class as a person who did not move. A clinical product then treats “the packet did not arrive” as “the user is at rest.”

**Robots and vehicles.** An occupancy map, a lidar filter, or a log player is expected to return a scene even when the sensor returned nothing. The planner then drives through a cell the sensor did not measure, because that cell now looks free.

三个产品卡在同一步。模型或地图被要求交回一幅完整场景，下一模块把这幅场景当成测到的。

世界模型这边，Cosmos 和 V-JEPA 2.1 的用法是“先想象下一帧，再行动”。交出去的画面没有洞。Nilaksh 等人说明，隐变量可以在像素上赢、在规划上输。Yuan 等人说明，能看到每个想象未来真实结果的先知，把成功率从 68.9% 抬到 79.2%，只给画面打分的选择器收不回这个差距。难点不是把未来画出来，而是画完之后看不出哪一块是猜的。Zhang 等人从另一侧说了同一件事：留下哪一个未来，动作就变了。

脑机接口这边，LaBraM 预测被遮住的脑电，InterpolatedLaBraM 保证检查点始终看到训练时的电极布局。丢失的数据包写成零，会被判成静息，和人没动是同一个类别。临床产品于是把“包没到”做成“用户在休息”。

机器人和车辆这边，占据栅格、激光滤波、日志回放都被期望在传感器没返回时仍交出一幅场景。规划器随后开过一个传感器没测到的格子，因为那个格子现在看起来是空的。

![The same split on a hand, a neural decoder, a mobile robot, and a vehicle.](docs/figures/hand-delta.png)
![Brain–computer interface.](docs/figures/bci-delta.png)
![Mobile robot.](docs/figures/robot-delta.png)
![Vehicle.](docs/figures/vehicle-delta.png)

## Where widely used open source still gives a number

These libraries are the ones a robotics or biosignal stack actually calls. On the input they were built for, they are right. On empty input they return a value the next function will accept. That value is then a decision.

这些库是机器人栈和生物信号栈真的会调用的。在它们被设计来接受的输入上，它们是对的。在空输入上，它们返回一个下一函数愿意接受的值。这个值随后就成了决策。

| Project | What empty input returns | Why that is a product problem |
|---|---|---|
| [MuJoCo 3.13.0](https://github.com/google-deepmind/mujoco) | an empty model loads | a scene with no bodies is still a scene |
| [munkres 1.1.4](https://github.com/bmc/munkres) | `[]` on `compute([[]])` ([issue 54](https://github.com/bmc/munkres/issues/54)) | “no assignment problem” looks like “assignment finished” |
| [NumPy 2.4.6](https://github.com/numpy/numpy) | norm `0.0`, mean `NaN` | a missing vector looks like a zero vector, or like a number that propagates quietly |
| [MNE-Python 1.9.0](https://github.com/mne-tools/mne-python) | duration 0, zero annotations | a missing recording looks like a silent recording |
| [NetworkX 3.6.1](https://github.com/networkx/networkx) | an empty graph has 0 nodes | “no map was loaded” looks like “the map is empty, so you are done” |
| [FilterPy 1.4.5](https://github.com/rlabbe/filterpy) | an empty update is accepted and the state stays `0.0` | “no lidar return” looks like “the state is zero” |
| [Foxglove MCAP](https://github.com/foxglove/mcap) | a log with zero messages | playback continues on silence |
| [ROS 2 rosbag2](https://github.com/ros2/rosbag2) | a bag with zero messages | same, for the bag a robot records |
| [pybloom-live 4.0.0](https://github.com/joseph-fox/python-bloomfilter) | a keyless filter reports non-membership | “no key was given” looks like “the key is absent” |

The shortcoming is the same in each row. Absence is stored as a number. The next module cannot tell “nothing was measured” from “the measurement was zero.”

每一行的不足是一样的。缺失被存成一个数。下一模块分不出“什么都没测到”和“测到的是零”。

On the same empty inputs this repository raises. On the occupied input the value is unchanged: a 2×2 assignment stays cost 2, the string `CAKE` stays distance 3, a recorded EEG clip stays 8 samples with markers `go` and `end`, one lidar pair counts as 1, three observations count as 3, and a three-cell chain reaches 2 in one step and 3 at the fixed point.

同样的空输入，这里直接拒绝。有内容的输入数值不变：2×2 指派代价仍是 2，`CAKE` 的距离仍是 3，一段实录脑电仍是 8 个采样、标记为 `go` 和 `end`，一对激光计数为 1，三次观测计数为 3，三格链走一步到达 2、走到不动点是 3。

## Why a boundary in front of the model is enough

We do not ship a new world model. The planner, the decoder, and the map library stay. The write that fills the hole is replaced by a function whose failure mode is proved, not trained.

我们不交付一个新的世界模型。规划器、解码器、地图库都留着。被换掉的是那个把洞填上的写入。它的失败方式是证明出来的，不是训练出来的。

Four statements. The proofs are in [`paper/paper.md`](paper/paper.md).

**The fill decides, the planner does not.** Run one shortest-path routine on a completed map and on the cells that were actually observed. The two calls return different integers. No change of generator is required for them to separate. A world-model reach of 3 against a measured step of 2, an EEG class of 0 against a recorded class of 1, and a myopic action of 0 against a lookahead action of 1 are the same fact in three products.

**Nested plans.** A pessimistic plan may enter only cells that were observed free. An optimistic plan may also enter masked cells. Every pessimistic path is therefore still legal after the fill, and it cannot be strictly shorter than the optimistic path. A score that prefers the shorter path, and on a tie prefers the optimistic one, returns the filled plan on every trial. On 2,000 grids the inclusion held on all 2,000. The oracle reaches 297 goals that this score misses. Of those 297, the filled path is strictly shorter on 129, and the two paths have equal length on 168. The 168 are the tie rule, not a shorter path. The 378 goals that only the filled plan reaches each step through a masked cell that was truly free: that is the set of goals a wall-fill refuses.

**The discount at which lookahead flips is a fraction.** On the trap table `[[10, 1], [-100, -100]]`, action 0 pays more now and steps into −100. Solving `(I − dP)V = r` in exact rationals gives the flip at `9/101`. Iterating a scaled integer backup flips too early, because the backup does not keep a common denominator. One real backup already matches the infinite horizon on this family. Depth 0 is the raw row. Treating that row as a backup reports the flip one step late.

**After the fill, a missing-data check sees nothing.** The completed object lives in the fully observed domain, so a checker that looks for a mask marker has recall 0. Empty input raises instead of returning 0. That is the entire product difference with the libraries in the table above.

四条陈述。证明在 [`paper/paper.md`](paper/paper.md)。

补全做决定，规划器不做决定。同一套最短路，在补全后的地图上跑一次，在真正观测到的格子上再跑一次，得到两个整数。不需要换生成器，这两个整数就会分开。世界模型可达 3 对实测一步 2，脑电类别 0 对实录类别 1，只看当前行的动作 0 对前视动作 1，是三个产品里的同一件事。

路径是嵌套的。悲观方案只能进入已观测为空的格子。乐观方案还可以进入被遮住的格子。所以每条悲观路径在补全之后仍然合法，而且不会严格短于乐观路径。偏好更短路径、平局时偏好乐观方案的分数，每次都返回补全后的方案。2,000 张图上包含关系全部成立。先知能到达、这个分数到不了的目标有 297 个。其中 129 次补全路径严格更短，168 次两条路一样长。168 是平局规则，不是更短。只有补全方案能到达的 378 个目标，每一条都踩过一个被遮住、实际上是空的格子。那是把遮挡当成墙时拒绝掉的目标。

前视把动作翻过来的折扣是一个分数。陷阱表 `[[10, 1], [-100, -100]]` 上，动作 0 眼前收益更高，下一步走进 −100。用精确有理数解 `(I − dP)V = r`，翻转点是 `9/101`。把折扣值放大成整数再迭代，会翻得太早，因为迭代保不住公分母。在这一族问题上，一次真正的回溯已经等于无限视界。深度 0 是原始的那一行。把那一行也算成一次回溯，翻转会晚报一步。

补全之后，缺失检查什么也看不见。补完的对象落在全观测的值域里，寻找掩码标记的检查召回率是 0。空输入会拒绝，而不是返回 0。这就是和上面那些库的全部产品差别。

![One split, three products. Filled input returns the larger integer. One measured step returns the smaller integer. Empty input raises.](docs/figures/story.png)

![Both plans reach on 122 grids. Only the filled plan reaches on 378. Only the safe plan reaches on 297, of which 129 are strictly shorter and 168 are ties. Neither reaches on 1,203.](docs/figures/partition.png)

## What the MVP hands over

The delivery is one call with three outcomes. It sits in front of a planner the product already runs.

交付是一次调用、三种结果。它坐在产品已经在跑的规划器前面。

| Call | What it does | What it refuses to do |
|---|---|---|
| `measure` | Uses only entries that were observed. On a map it does not enter a masked cell. On an EEG window it keeps the recorded samples. On a reward table it returns the lookahead action. | It does not invent a value for a hole. |
| `impute` | The audit twin. Same planner after the hole has been written free, written zero, or replaced by the visible row. | It is not the shipped decision. It exists so a demo can show the disagreement. |
| refuse | The result on empty input. | No zero, no empty list, no NaN. |

What a caller sees on the pinned demo:

| Input | Shipped decision | What a fill would have returned |
|---|---|---|
| Three cells, middle unseen | reach **2** | reach **3**, the fully observed map |
| Eight EEG samples, packet dropped and written as zeros | class **1** on the recorded samples | class **0**, identical to rest |
| Reward table, next action | lookahead action **1** | myopic action **0** |
| Empty input | raises | a usable number, in the libraries above |

Not in this MVP: a trained video model, a headset SDK, a robot success rate, or a claim that 68.9% and 79.2% were re-run. Those percentages belong to Yuan et al. The MVP shows the same kind of gap as an integer a reviewer can recompute.

这次 MVP 里没有：训练好的视频模型、头戴设备 SDK、机器人成功率，也没有“我们重跑了 68.9% 和 79.2%”这种说法。那两个百分比属于 Yuan 等人。MVP 把同一类差距做成一个可以重算的整数。

```bash
make check
python3.12 show_story.py
python3.12 show_policy.py
```

`make check` recomputes the pinned identities. The proofs and the method-by-method comparison with the papers above are in [`paper/paper.md`](paper/paper.md). Counts live in `results/`. Side-by-side callers need the versions in `requirements-show.txt`.

## Projects this boundary is meant to sit in front of

| Project | URL | Where the boundary attaches |
|---|---|---|
| [V-JEPA 2.1](https://arxiv.org/abs/2603.14482) | masked video tokens | do not treat a predicted patch as a measured cell |
| [Cosmos](https://github.com/nvidia-cosmos/cosmos-predict1) | predicted frames | same, for a rendered future |
| [LaBraM](https://arxiv.org/abs/2405.18765) | masked EEG | do not classify a zero-filled dropout as rest |
| NetworkX | https://github.com/networkx/networkx | one observed step versus the fixed point |
| MNE-Python | https://github.com/mne-tools/mne-python | a recording with no samples raises |
| MuJoCo | https://github.com/google-deepmind/mujoco | an empty model raises |
| Foxglove MCAP | https://github.com/foxglove/mcap | a log with no messages raises |
| ROS 2 rosbag2 | https://github.com/ros2/rosbag2 | a bag with no messages raises |
| ROS map_server | https://wiki.ros.org/map_server | unknown cells stay unknown |
| FilterPy | https://github.com/rlabbe/filterpy | an empty update raises |

The kernels that implement those refusals on the occupied formats are under `locks/`. The index is [`ATLAS.md`](ATLAS.md).

## Files

| Path | What the MVP calls |
|---|---|
| `tick.py` | one observed step |
| `datalog.py` | the fixed point a fill would return |
| `complete.py` · `decode.py` · `policy.py` | the three fills: map, EEG, reward row |
| `partition.py` | the inclusion check: shorter path versus tie |
| `paper/paper.md` | the theory, the way it was found, the comparison with each cited method |
| `tests/test_precision.py` | the identities the MVP is not allowed to move |

## License

MIT
