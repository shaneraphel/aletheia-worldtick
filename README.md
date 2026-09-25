# Worldtick · 世界一步

[![check](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml/badge.svg)](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml)

## 问题

2026 年的世界模型、脑电模型和动作模型，都在把没看见的地方补成一张完整的图，再用这张图做决定。V-JEPA 2.1 预测被遮住的视频块。Cosmos 和 VAE 把画面补到像素上看起来像。LaBraM 预测被遮住的脑电，缺的通道用插值补上。世界动作模型先画出下一步的画面，再从画面里选动作。

Nilaksh 等人在 [CVPR 2026 的工作](https://arxiv.org/abs/2605.06388)里写明：像素补得像，规划不一定对。Zhang 等人在 [2026 年的测试时规划](https://arxiv.org/abs/2609.24745)里写明：生成一个像样的未来，比从这些未来里选出该执行的动作更容易。

这里把这一个问题放进三个领域，用同一对整数来回答。补全得到较大的数，并且这个数可以和“真的看见了”相同。一步只使用已经看见的事实，得到较小的数。空记录报错。

## Problem

In 2026, world models, EEG models, and action models fill in what was not seen, then decide from the filled picture. V-JEPA 2.1 predicts masked video patches. Cosmos and VAEs complete the frame until the pixels look right. LaBraM predicts masked EEG, and missing channels are interpolated. World action models draw the next frame, then pick an action from that drawing.

Nilaksh et al., in a [CVPR 2026 workshop paper](https://arxiv.org/abs/2605.06388), state that a picture can look right while the plan is not. Zhang et al., on [test-time planning](https://arxiv.org/abs/2609.24745), state that producing a plausible future is easier than choosing the action that future supports.

The same question is asked here in three fields, and answered with one pair of integers. Completion returns the larger number, and that number can match a world that really was seen. One tick uses only a fact that was seen, and returns the smaller number. An empty record is an error.

![补全：世界模型可达 3，脑电类别 0，动作 0。一步：可达 2，类别 1，动作 1。洞、空包、空表报错。](docs/figures/story.png)

| | 补全 | 一步 | 空记录 |
|---|---|---|---|
| 世界模型，三格，中间是洞 | 可达 **3**，和一张全看见的地图相同 | 可达 **2** | 报错 |
| 脑电，8 个点 | 掉线补 0 之后类别 **0**，和静息相同 | 录上的点类别 **1**（go） | 报错 |
| 奖励表的下一动作 | 只看眼前这一行，动作 **0** | 走一步世界，动作 **1** | 报错 |

大地图上同一对结果是走一步 **24**、走到头 **214**。256×8 的奖励表上，眼前这一行是动作 **2**，走一步是动作 **5**。

On the large map the same pair is one tick **24** and the end of the walk **214**. On the 256×8 reward table the visible row is action **2** and one tick of the world is action **5**.

## 一万次 / 10,000 trials

种子 `20260919`，每条链 8 格，共 10,000 次。补全把洞写成 0。一步只从已经看见的格子出发。

Seed `20260919`. Each chain has 8 cells. 10,000 trials. Completion writes the hole as 0. One tick starts only from a cell that was seen.

![一万次：世界模型补全 8 与一步 2，脑电补零与静息同为 0，眼前动作 0 与走一步动作 1，全部 10000/10000。](docs/figures/campaign.png)

| | 补全 | 一步 | 次数 |
|---|---|---|---|
| 世界模型 | 可达 **8**，和补全后的整张图相同 | **2** | **10,000 / 10,000** |
| 脑电 | 掉线补 0 的类别是 **0**，和静息相同 | 录上的类别是 **1** | **10,000 / 10,000** |
| 下一动作 | 眼前这一行是动作 **0** | 走一步是动作 **1** | **10,000 / 10,000** |

数在 `results/CAMPAIGN.json`。`python3.12 campaign.py` 重算。

The counts are in `results/CAMPAIGN.json`. `python3.12 campaign.py` recomputes them.

2026 年这三篇工作的运算，就是上面的“补全”：

| 论文 | 他们的运算 | 这一万次里的结果 |
|---|---|---|
| [V-JEPA 2.1](https://arxiv.org/abs/2603.14482)（2026） | 被遮住的视频块也要预测出来 | 补上的格子可达 8；看见的一步是 2 |
| [Reconstruction or Semantics?](https://arxiv.org/abs/2605.06388)（CVPR 2026 workshop） | Cosmos / VAE 把画面补全；像素像，规划不一定对 | 补全后的可达数和一张全看见的地图相同 |
| [LaBraM](https://arxiv.org/abs/2405.18765) 与 [InterpolatedLaBraM](https://braindecode.org/dev/generated/braindecode.models.InterpolatedLaBraM.html) | 遮住的脑电块要预测；缺的通道被插值补上 | 补 0 的类别和静息相同，都是 0 |
| [Beyond Visual Quality](https://arxiv.org/abs/2609.24745)（2026） | 先生成未来画面，再从画面里选动作 | 眼前这一行选出的动作，和走一步选出的动作，10,000 次都不同 |

上表是这一万次的结果。比对的是这些论文共用的一步：把没看见的地方写成一个数。

## 补全之后会走进去的障碍

真的路上有障碍。传感器丢掉 30% 的格子。补全把丢掉的格子写成空地，然后往前走。一步停在第一个没看见的格子。

32 格，10,000 条路，种子 `20260919`。

![8564 条路藏着没看见的障碍。补全走进 2995 次。一步走进 0 次。](docs/figures/hidden.png)

| | 结果 |
|---|---|
| 藏着没看见的障碍 | **8,564 / 10,000** |
| 补全走进那处障碍 | **2,995** |
| 一步走进那处障碍 | **0** |

数在 `results/HIDDEN.json`。`python3.12 hidden.py` 重算。

## 洞越多，走进去的次数越多

每一点是 10,000 条 32 格的路。障碍率 0.20 不变。丢失率从 0.00 到 0.50。

![丢失率 0.00 到 0.50，补全走进去 0 到 5084 次，一步始终 0 次。](docs/figures/sweep.png)

| 丢失率 | 补全走进去 | 一步走进去 |
|---|---|---|
| 0.00 | **0** | **0** |
| 0.05 | **503** | **0** |
| 0.10 | **934** | **0** |
| 0.20 | **2,002** | **0** |
| 0.30 | **2,914** | **0** |
| 0.40 | **3,970** | **0** |
| 0.50 | **5,084** | **0** |

数在 `results/SWEEP.json`。`python3.12 sweep.py` 重算 70,000 条路。

Each point is 10,000 roads of 32 cells. Obstacle rate stays 0.20. Dropout runs 0.00 to 0.50. Completion walks in more often as the hole rate rises. One tick stays 0. Counts are in `results/SWEEP.json`. `python3.12 sweep.py` recomputes 70,000 roads.

## 走多少步收敛 / Horizon

同一张 256 节点图。步数从 0 放到 256。补全一次回答 214。

![步数 0 到 256，可达数 8、24、50、92、138、205、212，到 12 步收敛到 214。](docs/figures/horizon.png)

| 步数 horizon | 可达 reach |
|---|---|
| 0 | **8** |
| 1 | **24** |
| 2 | **50** |
| 3 | **92** |
| 4 | **138** |
| 6 | **205** |
| 8 | **212** |
| 12 | **214** |

12 步收敛，之后不动。数在 `results/HORIZON.json`。`python3.12 horizon.py` 重算。

One tick reaches 24. Twelve ticks reach the closure 214. Completion answers 214 in one call. Counts are in `results/HORIZON.json`. `python3.12 horizon.py` recomputes them.

## 远见从哪里翻转答案 / Foresight

陷阱表 `[[10,1],[-100,-100]]`：动作 0 眼前多 9 分，但走进 −100。折扣过 **9/101**，答案从动作 **0** 翻到动作 **1**。策略评估解 `(I−dP)V = r`，精确有理数，所以阈值是 sharp 的。

![折扣 0 到 0.95，0.05 之前是动作 0，0.10 之后是动作 1。红线是 9/101。一千张随机陷阱表全部翻转。](docs/figures/foresight.png)

| 折扣 discount | 动作 action |
|---|---|
| 0.00–0.08 | **0** |
| 0.09–0.95 | **1** |
| 随机陷阱表 1,000 张，折扣 0 对 0.9 | **1,000** 张翻转 |

数在 `results/FORESIGHT.json`。`python3.12 foresight.py` 重算。

The trap pays 10 now for action 0 and steps into −100. Past discount **9/101** the answer flips from action **0** to action **1**. Policy evaluation solves `(I−dP)V = r` in exact rationals, so the threshold is sharp. Counts are in `results/FORESIGHT.json`. `python3.12 foresight.py` recomputes them.

The true road has obstacles. The sensor drops 30% of the cells. Completion writes each drop as free space and walks on. One tick stops at the first unseen cell.

32 cells, 10,000 roads, seed `20260919`.

| | result |
|---|---|
| roads with an unseen obstacle | **8,564 / 10,000** |
| completion walks into that obstacle | **2,995** |
| one tick walks into that obstacle | **0** |

The counts are in `results/HIDDEN.json`. `python3.12 hidden.py` recomputes them.

The table is the result of these 10,000 trials. The comparison is the step those papers share: writing a number into a place that was not seen.

Completion writes a usable number into a place that was not seen. One tick moves only a fact that was already seen. The three fields above give that pair.

| | completion | one tick | empty record |
|---|---|---|---|
| world model, three cells, a hole in the middle | reach **3**, the same integer as a fully seen map | reach **2** | error |
| EEG, 8 samples | a dropped packet filled with zeros is class **0**, the same integer as rest | the recorded samples are class **1** (go) | error |
| next action on a reward table | the visible row alone is action **0** | one tick of the world is action **1** | error |

## 灵巧手 / Dexterous hand

![空的手：MuJoCo 加载成功，munkres 返回空列表，这里报错。有数字的 2×2 表，代价 2。](docs/figures/hand-delta.png)

| 输入 | 结果 |
|---|---|
| [MuJoCo 3.13.0](https://github.com/google-deepmind/mujoco) 空模型 | 加载成功 |
| [munkres 1.1.4](https://github.com/bmc/munkres) 空表 `compute([[]])` | 空列表 `[]`（[issue 54](https://github.com/bmc/munkres/issues/54)） |
| 同一张空表 | 报错 |
| 2×2 抓取表 | 代价 **2** |
| 两指，字母 `CAKE` | 距离 **3** |
| [NumPy 2.4.6](https://github.com/numpy/numpy) 空向量长度 | `0.0` |

[`locks/aletheia-handlock`](locks/aletheia-handlock) · [`locks/aletheia-fingerlock`](locks/aletheia-fingerlock)

## 脑机接口 / Brain-computer interface

![空录音：MNE 时长 0、标记 0，NumPy 平均值为 nan，这里报错。录上的一段是 8 个点，标记 go / end。](docs/figures/bci-delta.png)

| 输入 | 结果 |
|---|---|
| [MNE-Python 1.9.0](https://github.com/mne-tools/mne-python) 空录音 | 时长 0，标记个数 0 |
| [NumPy 2.4.6](https://github.com/numpy/numpy) 空采样的平均 | `nan` |
| 同一段空录音，空的标记表 | 报错 |
| 录上的一段 | **8** 个点，标记 `go` / `end` |
| 存进去的平坦采样（速率 0） | 仍是一条采样 |
| [pybloom-live 4.0.0](https://github.com/joseph-fox/python-bloomfilter) 没有键的过滤器 | “不是成员” |
| 空的键列表 | 报错 |

[`locks/aletheia-spikelock`](locks/aletheia-spikelock) · [`locks/aletheia-bloomlock`](locks/aletheia-bloomlock)

一万个随机 go 包，每包 8 个点。丢掉后 k 个点并补零。被读成静息的个数：

![丢 0 到 8 个点，被读成静息 0、0、1、9、43、161、642、2494、10000。](docs/figures/bcisweep.png)

| 丢掉 | 读成静息 |
|---|---|
| 0 | **0** |
| 4 | **43** |
| 7 | **2,494** |
| 8 | **10,000** |

数在 `results/BCISWEEP.json`。`python3.12 bcisweep.py` 重算。

Ten thousand random go packets of 8 samples. Drop the last k samples and fill zeros. Packets read as rest: 0, 0, 1, 9, 43, 161, 642, 2494, 10000. Counts are in `results/BCISWEEP.json`. `python3.12 bcisweep.py` recomputes them.

## 移动机器人 / Mobile robot

![三格地图：空图地点数 0；有路时 NetworkX 一次得到 3。空的一步报错。走一步 2，走到头 3。大地图 24，然后 214。](docs/figures/robot-delta.png)

| 输入 | 结果 |
|---|---|
| [NetworkX 3.6.1](https://github.com/networkx/networkx) 空图 | 地点个数 0 |
| 同一条三格的路 | 一次得到 **3** |
| 路还在，这一步是空的 | 报错 |
| 1×3 地图，走一步 | **2** |
| 1×3 地图，走到头 | **3** |
| 256 个地点，8 个起点，512 条路，种子 `20260919`，走一步 | **24** |
| 同一张图，走到头，两遍 | **214** 和 **214** |
| 步数放到 256 | **214** |
| 广度优先搜索，走到头 | **214** |

[`tick.py`](tick.py) · [`datalog.py`](datalog.py) · [`occgrid.py`](occgrid.py)

## 车 / Vehicle

![空雷达：NumPy 长度 0.0，FilterPy 位置留在 0.0，这里报错。两个点算作 1，三次观测算作 3。](docs/figures/vehicle-delta.png)

| 输入 | 结果 |
|---|---|
| [NumPy 2.4.6](https://github.com/numpy/numpy) 空雷达的长度 | `0.0` |
| [FilterPy 1.4.5](https://github.com/rlabbe/filterpy) 空更新 | 接受，位置 `0.0` |
| 同一帧空雷达，同一次空观测 | 报错 |
| 两个雷达点 | **1** |
| 三次观测 | **3** |
| [NetworkX](https://github.com/networkx/networkx) 没有节点的路图 | 地点个数 0 |
| 没有站点的路线 | 报错 |

[`locks/aletheia-voxelock`](locks/aletheia-voxelock) · [`locks/aletheia-kalmanlock`](locks/aletheia-kalmanlock) · [`locks/aletheia-tourlock`](locks/aletheia-tourlock)

## 奖励表 / Reward table

| 输入 | 结果 |
|---|---|
| 两行表，只看第 0 行最大的格子 | 动作 **0** |
| 同一张表，把下一步的分数打九折加回来 | 动作 **1** |
| 256 个状态 × 8 个动作，种子 `20260919`，只看第 0 行 | 动作 **2** |
| 同一张表，看下一步，两遍 | 动作 **5** 和 **5** |
| 空的奖励表 | 报错 |

## 日志 / Logs

| 输入 | 结果 |
|---|---|
| [map_server](https://wiki.ros.org/map_server) 空白格子图 | 报错 |
| [MCAP](https://github.com/foxglove/mcap) 零条消息 | 报错 |
| [rosbag2](https://github.com/ros2/rosbag2) 零条消息 | 报错 |
| NetworkX 三节点图，边还在、起点是空的 | 报错 |

## 运行 / Run

```bash
make check
python3.12 show_tick.py
python3.12 show_policy.py
python3.12 show_networkx.py
```

数在 `results/`。`make check` 重算该相等的几项。每次推送同样重算。

Numbers are in `results/`. `make check` recomputes the ones that match. Every push recomputes them.

## 上游 / Upstream

| 项目 | 地址 | 结果 |
|---|---|---|
| NetworkX | https://github.com/networkx/networkx | 空图地点数 0；三格的路一次得到 3 |
| Foxglove MCAP | https://github.com/foxglove/mcap | 零条消息：报错 |
| ROS 2 rosbag2 | https://github.com/ros2/rosbag2 | 零条消息：报错 |
| rosbags | https://gitlab.com/ternaris/rosbags | `show_rosbags.py` 的读取结果 |
| ROS map_server | https://wiki.ros.org/map_server | 空白格子图：报错 |
| OccupancyGrid | https://docs.ros.org/en/humble/p/nav_msgs/interfaces/msg/OccupancyGrid.html | 空白格子图：报错 |
| ROS 2 | https://github.com/ros2/ros2 | 上面的包和地图 |
| Soufflé | https://github.com/souffle-lang/souffle | 走到头这一类推法；这张固定地图的结果是 214 |
| NumPy | https://github.com/numpy/numpy | 空平均 `nan`；空长度 `0.0` |
| MNE-Python | https://github.com/mne-tools/mne-python | 空录音时长 0，标记个数 0 |
| BIDS | https://github.com/bids-standard/bids-specification | 只有表头的事件表：报错 |
| NiBabel | https://github.com/nipy/nibabel | NIfTI，见 [`ATLAS.md`](ATLAS.md) |
| OpenDRIVE | https://github.com/asam-oss/asamOpenDRIVE | 空路口图：报错 |
| MuJoCo | https://github.com/google-deepmind/mujoco | 空模型：加载成功 |
| Open3D | https://github.com/isl-org/Open3D | 与雷达点一起的结果：1 |
| nuScenes | https://github.com/nutonomy/nuscenes-devkit | 空样本：报错 |
| pyahocorasick | https://github.com/WojciechMula/pyahocorasick | 空文本上的对照 |
| python-bloomfilter | https://github.com/joseph-fox/python-bloomfilter | 没有键：不是成员。空键列表：报错 |

## 文件 / Files

| 路径 | 结果所在 |
|---|---|
| `tick.py` | 走一步：2，以及 24 |
| `datalog.py` | 走到头：3，以及 214 |
| `policy.py` | 动作 0 / 1，以及 2 / 5 |
| `occgrid.py` | 1×3 格子图 |
| `mcapocc.py` | MCAP |
| `bagocc.py` | rosbag2 |
| `locks/` | 66 个格式上的结果 |
| `binds/` | 100 条带名字的记录 |
| [`ATLAS.md`](ATLAS.md) | 目录 |

## License / 许可

MIT
