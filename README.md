# Worldtick

[![check](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml/badge.svg)](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml)

A boundary in front of a world model, a neural decoder, or a planner. Cells that were not observed stay unobserved. Empty input is refused, and does not come back as zero.

放在世界模型、神经解码器或规划器前面的一道边界。没观测到的格子保持没观测到。空输入被拒绝，不会变成 0。

可以打开的页面：[shaneraphel.github.io/aletheia-worldtick](https://shaneraphel.github.io/aletheia-worldtick/)。

## How to read this

Read in this order. The page is the product. This file is the reason the product is shaped that way. The proofs are a separate note.

1. Open the page and press the three buttons on the corridor, then the EEG window, then the reward row. Do this before reading any count.
2. If a word is unfamiliar, use the list below. The same word means the same thing in the page, in this file, and in the note.
3. Read where shipped products get stuck, then where common libraries still return a number. That is the problem the page is for.
4. Read why a check in front of the model is enough. The counts there are witnesses of those statements, not a separate result.
5. The proofs, and the comparison with each cited method, are in [`paper/paper.md`](paper/paper.md).

按这个顺序读。页面是产品。这份文件说明产品为什么是这个形状。证明在另一份笔记里。

1. 先打开页面，按走廊上的三个按钮，再看脑电窗口，再看奖励表。在看任何计数之前做完这一步。
2. 有不认识的词，用下面的名单。同一个词在页面、这份文件和笔记里是同一个意思。
3. 再读业界产品卡在哪里，以及常用的库为什么仍会交回一个数。那就是这个页面要处理的问题。
4. 再读为什么模型前面的一道检查就够。那里的计数是这些陈述的见证，不是另一项结果。
5. 证明，以及和每篇参考文献的方法对照，在 [`paper/paper.md`](paper/paper.md)。

A team funded to ship a video world model spends the work on data, training, and a robot test. That is the generator. This repository ships the check in front of the generator. The two do not share a schedule, because they are not the same product. The check is a page and a library call. It does not train anything, and it does not claim the generator's robot score.

拿融资去做视频世界模型的团队，时间花在数据、训练和机器人测试上。那是生成器。本仓库交付的是生成器前面的检查。两件事不是同一张时间表，因为它们不是同一个产品。检查是一个页面和一次库调用。它不训练，也不声称自己有生成器的机器人分数。

We do not post the page on another project's issue tracker. Those issues are for defects in that project. A comment that is really a product announcement gets removed, and it should. When a library has an empty-input defect we can fix with a test, the contribution is a pull request.

我们不把页面发到别的项目的 issue 里。那些 issue 是为了那个项目自己的缺陷。一条实际内容是产品公告的评论会被删掉，也应该被删掉。某个库在空输入上确有缺陷、而且我们能用测试修好时，贡献的形式是一个 pull request。

## Words

| Word | Meaning |
|---|---|
| Partial observation | Some entries of the input were not measured. They are not the same thing as a measured zero. |
| Fill, imputation | Writing a usable value into an entry that was not measured, then treating the result as if it had been measured. |
| Optimistic fill | The written value is “free” on a map, or zero on a signal. The hole disappears. |
| Pessimistic fill | The written value is “blocked.” The planner may not enter a cell it did not see. |
| Measured step | A transition that uses only entries that were actually observed. An unseen cell is not entered. |
| Mask | The mark that an entry was not observed. A fill deletes this mark. After the fill, a checker that looks for the mark finds nothing. |
| Empty input | An input with nothing in it. Here it is refused. It is not returned as zero, as an empty list, or as not-a-number. |
| Tie | Two plans with the same length. On a tie, the shipped decision keeps the plan that uses only observed free cells. |
| Oracle | A score that knows which plan hits a real obstacle. It is a reference, not a sensor the product has at deployment. |
| Discount `9/101` | The point at which one backup changes the action on the trap table. Below it, the visible row wins. Above it, the backup wins. |
| Fixed point | The set of everything reachable if the walk is allowed to finish. One step is a smaller set. Returning the fixed point in one call reports the finished walk as the present. |
| One question | Blocking the first cell where the filled path crashes, then planning again. It does not repair the other unseen cells. |
| Closed loop | Observing again before every step, instead of trusting the rest of the fill. |
| Scene hold | The music and the picture stay as they are, because the brain window was incomplete. A class computed after filling that window is not allowed to change them. |
| Bilateral sound | Alternating left-right sound, the sensory part of an EMDR session. This repository does not claim a treatment effect. The rule is when that sound may change. |
| Grasp picture | The 3D picture of a dexterous hand in the scene. It may not show a finished grasp through a cell the camera did not see. |
| Silent file | A sound file with zero frames. Players open it. The session does not treat it as rest. |
| Empty cloud | A point cloud or mesh with nothing in it. Geometry libraries return it. The session does not treat it as a finished hand. |

| 词 | 意思 |
|---|---|
| 部分观测 | 输入里有些项没有测到。它们不是“测到了零”。 |
| 补全 | 给没测到的项写上一个能用的值，然后把结果当成测到的。 |
| 乐观补全 | 在地图上写成空地，在信号上写成零。洞消失了。 |
| 悲观补全 | 写成挡住。规划器不能进入没看见的格子。 |
| 实测步 | 只用真正观测到的项做一次转移。没看见的格子不进入。 |
| 掩码 | “这一项没观测到”的标记。补全会删掉这个标记。补完之后，寻找这个标记的检查什么也找不到。 |
| 空输入 | 里面什么都没有的输入。这里直接拒绝。不返回零，不返回空列表，也不返回非数。 |
| 平局 | 两条路一样长。平局时，交出去的决策留下只走已观测空地的那条。 |
| 先知 | 知道哪条路会撞上真障碍的分数。它是参照，不是产品在部署时拥有的传感器。 |
| 折扣 `9/101` | 在陷阱表上，一次回溯改变动作的那个点。低于它，当前行赢。高于它，回溯赢。 |
| 不动点 | 如果把路走完，所有能到达的位置。一步比它小。一次调用就返回不动点，是把走完的路当成了现在。 |
| 一次追问 | 封住补全路径第一次撞上的格子，再规划一次。它不修理其余没看见的格子。 |
| 闭环 | 每走一步之前再观测一次，而不是相信补全剩下的部分。 |
| 画面保持 | 音乐和画面维持原样，因为脑电窗口不完整。用补全后的类别去改它们，是不允许的。 |
| 双侧声音 | 左右交替的声音，是 EMDR 里的感觉部分。本仓库不声称治疗效果。规则只规定这段声音什么时候可以变。 |
| 抓取画面 | 灵巧手在场景里的三维画面。它不能把摄像机没看见的格子画成一次已经完成的抓取。 |
| 无声文件 | 帧数为 0 的声音文件。播放器会打开它。会话不把它当成静息。 |
| 空点云 | 里面没有点的点云或网格。几何库会把它交回来。会话不把它当成一只已经成形的手。 |

## Two people, one picture

The page is aimed at two groups, and both are injured by the same write.

**Someone adapting to a dexterous hand.** The world model is there to show the hand in the scene, in real time, so the person can see a reach before the hand has finished it. The failure is a picture of a grasp that passes through a cell the camera did not see. The person then practices a motion the world does not contain. On 2,000 maps the filled picture does this 1,439 times. The coach draws that completed grasp 0 times.

**Someone staying with a bilateral sound.** EMDR pairs recall with a left-right sound. The practical difficulty is that the sound is hard to stay with, so the game is an open place where that sound can continue, and where other people are present at low demand. A world model can also be asked to change the sound and the picture when a brain window looks frightened. If that window was incomplete and then filled with zeros, the change is not a reading of fright. On 10,000 signed windows with the last 4 samples dropped, a zero-fill would retune 2,421 of them: 1,280 movements read as rest, and 1,141 rests read as movement. The session holds all 10,000. It does not claim that holding treats anyone.

The world model is the picture. The non-invasive window is a partial observation. The hand camera is a partial observation. Filling either one, and then letting the picture move, is the same decision this repository already refuses on a map, on an EEG packet, and on a reward row.

一个人在适应灵巧手。世界模型用来把这只手画进场景，让人在手还没走完时看见这一下。失败的画面是一次抓取穿过了摄像机没看见的格子。人会按一幅世界里并不存在的动作去练。2,000 张图上，补全后的画面这样做了 1,439 次。引导把这种“已经抓完”画出来的次数是 0。

一个人留在一段双侧声音里。EMDR 把回忆和左右交替的声音放在一起。实际的困难是这段声音很难听下去，所以游戏是一个开放的地方，声音可以在那里继续，别人也可以在场，但不要求高消耗的社交。世界模型还可能被要求：脑电窗口看起来像惊恐时，就改声音和画面。如果那个窗口不完整，又被补成了零，这次改动就不是对惊恐的读取。10,000 个有符号窗口丢掉最后 4 个采样，补零会改掉其中 2,421 个：1,280 个动作被读成静息，1,141 个静息被读成动作。会话对这 10,000 个窗口全部保持。它不声称保持本身在治疗谁。

世界模型是那幅画面。非侵入窗口是一次部分观测。手上的摄像机也是一次部分观测。补上其中任何一个，再让画面动起来，就是本仓库在地图、脑电和奖励表上已经拒绝的同一个决策。

![An incomplete window would retune 2,421 sounds. The session holds all 10,000. A filled grasp crosses an obstacle 1,439 times. The coach draws that 0 times.](docs/figures/session.png)

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
| Python `wave` | a file with **0** frames is a legal sound | silence with a sample rate is still a sound the next player will open |
| [SciPy 1.17.1](https://github.com/scipy/scipy) | an empty array written as WAV comes back with shape `(0,)` at 8,000 Hz | a dropped bilateral tone is a readable file |
| [soundfile 0.14.0](https://github.com/bastibe/python-soundfile) | the same empty WAV reads as length 0 | same, for the library a game uses to play it |
| [Pillow 11.3.0](https://github.com/python-pillow/Pillow) | `Image.new` accepts a **0×0** RGB image | a world-model frame can exist with no pixels |
| [OpenCV 5.0.0](https://github.com/opencv/opencv) | an empty image has **0** nonzero pixels | “nothing was seen” looks like a counted zero |
| [Open3D 0.20.0](https://github.com/isl-org/Open3D) | an empty cloud has **0** points and an empty mesh has **0** vertices | a hand scan that did not arrive is still a geometry object |

The shortcoming is the same in each row. Absence is stored as a number. The next module cannot tell “nothing was measured” from “the measurement was zero.”

每一行的不足是一样的。缺失被存成一个数。下一模块分不出“什么都没测到”和“测到的是零”。

声音、画面和点云是同一种形状。合法的文件可以有 0 帧，合法的图像可以是 0×0，合法的点云可以有 0 个点。8 个采样的一段声音类别是 1。空的采样会拒绝。同一批 2,000 张手部地图，单核和 10 个核数出来的碰撞都是 1,439。

A sound file, a frame, and a cloud have the same shape. A legal file can hold 0 frames, a legal image can be 0×0, and a legal cloud can hold 0 points. An 8-sample tone is class 1. Empty samples raise. The same 2,000 hand maps crash 1,439 times on one core and on 10 cores.

![Empty sound, blank image, empty cloud.](docs/figures/media.png)

![Serial crashes 1,439. Parallel crashes 1,439. Ten workers.](docs/figures/fleet.png)

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

证明在 [`paper/paper.md`](paper/paper.md)。

补全做决定，规划器不做决定。同一套最短路，在补全后的地图上跑一次，在真正观测到的格子上再跑一次，得到两个整数。不需要换生成器，这两个整数就会分开。世界模型可达 3 对实测一步 2，脑电类别 0 对实录类别 1，只看当前行的动作 0 对前视动作 1，是三个产品里的同一件事。

路径是嵌套的。悲观方案只能进入已观测为空的格子。乐观方案还可以进入被遮住的格子。所以每条悲观路径在补全之后仍然合法，而且不会严格短于乐观路径。偏好更短路径、平局时偏好乐观方案的分数，每次都返回补全后的方案。2,000 张图上包含关系全部成立。先知能到达、这个分数到不了的目标有 297 个。其中 129 次补全路径严格更短，168 次两条路一样长。168 是平局规则，不是更短。只有补全方案能到达的 378 个目标，每一条都踩过一个被遮住、实际上是空的格子。那是把遮挡当成墙时拒绝掉的目标。

前视把动作翻过来的折扣是一个分数。陷阱表 `[[10, 1], [-100, -100]]` 上，动作 0 眼前收益更高，下一步走进 −100。用精确有理数解 `(I − dP)V = r`，翻转点是 `9/101`。把折扣值放大成整数再迭代，会翻得太早，因为迭代保不住公分母。在这一族问题上，一次真正的回溯已经等于无限视界。深度 0 是原始的那一行。把那一行也算成一次回溯，翻转会晚报一步。

**A tie is not indifference.** When the two paths have the same length, the observed-free path exists, so it arrives. Switching the tie from the filled plan to that path recovers every tied miss and gives up none of the goals that only the filled plan can reach, because those goals have no second path. The misses that remain are the paths that became shorter by crossing a masked cell. Most of those shorter paths still crash. Length is not a safety certificate.

**Zero is not “nothing happened.”** On a non-negative code, writing zeros can only turn a movement into rest. On a signed voltage, erasing a negative sample can turn rest into a movement. A decoder that zero-fills a dropout is not choosing the conservative error. The direction of the error is the sign of the samples it deleted. LaBraM-style interpolation has the same shape: the filled window is a decision, and the missingness is gone.

平局不是“两条路都行”。两条路一样长时，已观测为空的那条路存在，所以它能到达。把平局从补全方案改判给这条路，能收回每一次平局造成的错过，而且不会丢掉只有补全方案能到达的目标，因为那些目标根本没有第二条路。剩下的错过，是靠踩被遮格子才变短的路。这些更短的路里，多数仍然会撞。更短不是安全证明。

零不是“什么都没发生”。信号非负时，补零只能把动作读成静息。电压有正负时，删掉一段负数可以把静息读成动作。把丢包补成零的解码器并没有选择更保守的错误。错误的方向等于被删采样的符号。LaBraM 那种插值是同一形状：补完的窗口已经是一个决策，缺失本身消失了。

补全之后，缺失检查什么也看不见。补完的对象落在全观测的值域里，寻找掩码标记的检查召回率是 0。空输入会拒绝，而不是返回 0。这就是和上面那些库的全部产品差别。

![One split, three products. Filled input returns the larger integer. One measured step returns the smaller integer. Empty input raises.](docs/figures/story.png)

![Both plans reach on 122 grids. Only the filled plan reaches on 378. Only the safe plan reaches on 297. A tie, switched to the observed-free path, recovers the tied misses and none of the 378.](docs/figures/partition.png)

![Non-negative codes: false go is zero. Signed voltages, last four samples zeroed: false rest and false go both occur.](docs/figures/signfill.png)

## What the MVP hands over

The delivery is one call with three outcomes. It sits in front of a planner the product already runs.

交付是一次调用、三种结果。它坐在产品已经在跑的规划器前面。

| Call | What it does | What it refuses to do |
|---|---|---|
| `measure` | Uses only entries that were observed. On a tie between a filled path and an observed-free path, it keeps the observed-free path. On a signed EEG window it does not write zeros over a dropout. | It does not invent a value for a hole, and it does not break a tie toward the filled plan. |
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

## The page a person can open

The thing to hand someone is a static page: [`site/index.html`](site/index.html). It runs the three decisions in the browser. The map, the EEG window, and the reward row each show the filled answer next to the measured answer. Nothing on that page is trained.

一个人可以打开的东西是一个静态页面：[`site/index.html`](site/index.html)。三个决策在浏览器里算完。地图、脑电窗口、奖励表，各自把补全后的答案和实测答案摆在一起。这个页面上没有训练。

A team that raises a round to build a video world model is building the generator. This page is the check in front of that generator. The check is a file because every shipped decision is an integer with a proof. The generator is a different program, with data, training, and a robot evaluation that this MVP does not pretend to replace.

拿一轮融资去做视频世界模型的团队，做的是生成器。这个页面是放在生成器前面的检查。检查可以是一个文件，因为交出去的每个决策都是一个有证明的整数。生成器是另一件事，需要数据、训练和机器人评估。这个 MVP 不假装替代那件事。

One question is not that check. On the same 2,000 grids, the filled plan crashes 1,439 times. Blocking the first crash cell, then planning again, lets 614 paths arrive and leaves 786 crashing on a later masked cell. The page shows a five-cell corridor with the same shape: fill crashes, one question crashes again, the measured step never enters the unseen cell.

一次追问不是这个检查。同样的 2,000 张图上，补全方案撞了 1,439 次。封住第一次撞上的格子再规划，614 条路能到，786 条在后面另一个被遮格子上再撞。页面上有一条五格走廊，形状相同：补全会撞，问过一次还会撞，实测步不进入没看见的格子。

![After one question: 614 reach, 786 crash again, 39 stop.](docs/figures/decisive.png)

Asking until the path is clear does not stop at one. Of 2,000 grids, 561 need no question, 653 are done in one, and 786 need more than one. The questions total 2,814. One grid needs 9. The 786 is the majority of the grids that crash, not a thin tail.

一直问到路能走通或者无路可走，并不会停在一次。2,000 张图里，561 张不用问，653 张问一次就结束，786 张要问多于一次。追问合计 2,814 次。有一张图要问 9 次。这 786 张是会撞的图里的多数，不是一条细尾巴。

![Questions until the path is clear. Most crashing grids need more than one.](docs/figures/askdepth.png)

The page deploys as a GitHub Pages site from this repository. It does not ask for an account.

We do not post it on another project's issue tracker. Those issues are for defects in that project. A comment whose real content is a product announcement gets removed, and it should. When one of those libraries has an empty-input defect we can fix with a test, the contribution is a pull request. Traffic for this boundary is the page and this README.

页面用本仓库的 GitHub Pages 发布，不需要账号。

我们不把它发到别的项目的 issue 里。那些 issue 是为了那个项目自己的缺陷。一条实际内容是产品公告的评论会被删掉，也应该被删掉。某个库在空输入上确有缺陷、而且我们能用测试修好时，贡献的形式是一个 pull request。这个边界的流量来自这个页面和这份 README。

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
| `partition.py` | nested plans, and the tie rule |
| `signfill.py` | zero-fill on non-negative codes versus signed voltages |
| `decisive.py` | one question after the first crash |
| `askdepth.py` | how many questions until the path is clear |
| `session.py` | hold the sound on a dropped window; do not draw a grasp through an unseen cell |
| `fleet.py` | the same 2,000 maps on one core and on many; the crash count matches |
| `media.py` | empty WAV, empty image, empty cloud, beside a held session |
| `site/index.html` | the page that runs the three decisions in the browser |
| `paper/paper.md` | the theory, the way it was found, the comparison with each cited method |
| `tests/test_precision.py` | the identities the MVP is not allowed to move |

## License

MIT
