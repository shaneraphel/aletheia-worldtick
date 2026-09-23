# Worldtick · 世界一步

[![check](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml/badge.svg)](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml)

## 这是什么

机器人、车、灵巧手和脑机接口，都会把“刚才看到了什么”记下来。这份记录可能是一张格子地图，一段脑电，一帧雷达，或者一张“哪根手指去碰哪个点”的表。

记录有时是空的。传感器掉线了。日志里一条消息都没有。手指还没碰到任何东西。脑电帽戴着，这一段却没录上。

常用的开源库遇到这种空记录，常常给一个能继续算下去的答案：0，0.0，空列表，或者一个叫 nan 的“不是数”。后面的程序就接着走，好像世界是空的、是安全的、代价是零。

Worldtick 在这里停下来，告诉调用者：这份记录是缺的，不要把它当成 0。记录里真有内容时，算出来的数保持原样。我们没有去改那些开源库自己的仓库。做法是拿同一份输入，并排调用一次：他们返回 0 或空列表，我们报错。

下面四张图，每张都是这件事。左边是产品长什么样，右边是同一次运行里记下的结果。数字抄自仓库里的 JSON，可以按文末的命令再跑一遍。

## What this is

A robot, a car, a dexterous hand, and a brain-computer interface all keep a record of what they just saw. That record might be a grid map, an EEG clip, one lidar frame, or a table that says which finger should touch which point.

Sometimes the record is empty. The sensor dropped. The log has no messages. The fingers have not touched anything. The cap is on, and this clip was never recorded.

Widely used open-source libraries often answer that empty record with something a program can keep using: 0, 0.0, an empty list, or nan. The next program continues, as if the world were clear, safe, and free.

Worldtick stops and says the record is missing. When the record really has contents, the number stays the number it was. We do not edit those upstream repositories. We call their function and ours on the same input. Theirs returns 0 or an empty list. Ours reports an error.

Each picture below is that comparison. The left side is the product. The right side is the result written down in the same run. The numbers are copied from JSON files in this repo, and the commands at the end recompute them.

## 灵巧手

![手指还没碰到任何东西。MuJoCo 把空模型当成加载成功，munkres 返回空列表。这里停下来报错。表里有数字时，代价仍是 2。](docs/figures/hand-delta.png)

一只五指的手要去抓两个点。软件要回答：哪根手指去哪个点，总代价最小。

[MuJoCo](https://github.com/google-deepmind/mujoco) 是做机器人仿真的。我们给 3.13.0 一个没有身体的空模型，它加载成功。[munkres](https://github.com/bmc/munkres) 1.1.4 是做这种分配的。我们给它一张里面什么都没有的表，它返回一个空列表。他们自己在 [issue 54](https://github.com/bmc/munkres/issues/54) 里讨论过这种空表。空列表很容易被后面的程序读成“分配做完了，没有代价”。

同一张空表，我们的程序停下来报错。表里真有四个数时，最小代价仍是 **2**。

还有一个两根手指的例子。手指要在字母 `CAKE` 上找最短的间隔，答案是 **3**。字母是空的时候，[NumPy](https://github.com/numpy/numpy) 2.4.6 把向量长度算成 `0.0`。我们停下来，不把“没有字母”写成距离 0。

代码在 [`locks/aletheia-handlock`](locks/aletheia-handlock) 和 [`locks/aletheia-fingerlock`](locks/aletheia-fingerlock)。

A five-finger hand is reaching for two points. The software has to say which finger goes to which point so the total cost is smallest.

[MuJoCo](https://github.com/google-deepmind/mujoco) simulates robots. Version 3.13.0 loads a model that has no body and treats that load as a success. [munkres](https://github.com/bmc/munkres) 1.1.4 assigns fingers to points. Given a table with nothing in it, it returns an empty list. Their [issue 54](https://github.com/bmc/munkres/issues/54) is about that empty table. An empty list is easy for the next program to read as “the assignment is done, and it cost nothing.”

On that same empty table, our program stops and reports an error. When the table really holds four numbers, the smallest cost is still **2**.

A second example uses two fingers on the letters `CAKE`. The shortest gap is **3**. When the letters are missing, [NumPy](https://github.com/numpy/numpy) 2.4.6 reports a length of `0.0`. We stop, and we do not write that missing word down as distance 0.

The code is in [`locks/aletheia-handlock`](locks/aletheia-handlock) and [`locks/aletheia-fingerlock`](locks/aletheia-fingerlock).

## 脑机接口

![这段脑电其实没录上。MNE 把空录音的时长记成 0，NumPy 得到 nan。这里停下来报错。录上的一段仍是 8 个点，标记仍是 go / end。](docs/figures/bci-delta.png)

头上戴着电极帽，屏幕上应该有一条脑电。研究者还要知道这一段是“开始”（go）还是“结束”（end）。

[MNE-Python](https://github.com/mne-tools/mne-python) 1.9.0 是读脑电文件的常用库。一段空录音在它那里的时长是 0，标记个数也是 0。时长 0 看起来像“录了一段，里面是静音”。[NumPy](https://github.com/numpy/numpy) 2.4.6 对一个空数组求平均，得到 nan。nan 会顺着后面的统计继续传。

同一段空录音，我们停下来报错。真正录上的那一段仍是 **8** 个采样点，标记仍是 `go` 和 `end`。一个存进去的 0（直流、没有波动）仍是一个真实采样，不会被当成“这段没录”。

过滤器也一样。[pybloom-live](https://github.com/joseph-fox/python-bloomfilter) 4.0.0 对一个没有任何键的过滤器说“不是成员”。这和“查过了，确实不在”长得一样。我们遇到空的键列表会停下来。

代码在 [`locks/aletheia-spikelock`](locks/aletheia-spikelock) 和 [`locks/aletheia-bloomlock`](locks/aletheia-bloomlock)。文件格式包括 EDF、BIDS-EEG、XDF、BrainVision、WFDB、GDF。

The cap is on, and the screen should show an EEG trace. A researcher also needs to know whether this clip is a start (`go`) or an end (`end`).

[MNE-Python](https://github.com/mne-tools/mne-python) 1.9.0 is the usual library for reading those files. An empty recording has duration 0 there, and the marker count is 0. Duration 0 looks like “we recorded a clip, and it was silence.” [NumPy](https://github.com/numpy/numpy) 2.4.6 averages an empty array and returns nan. That nan keeps flowing into the next statistic.

On that same empty recording, we stop and report an error. The clip that really was recorded is still **8** samples, and the markers are still `go` and `end`. A stored 0, a flat DC sample, stays a real sample. It is not treated as “this clip was never recorded.”

The same split shows up in a filter. [pybloom-live](https://github.com/joseph-fox/python-bloomfilter) 4.0.0 says “not a member” for a filter that has no keys. That looks like a real lookup that came back no. An empty key list makes us stop.

The code is in [`locks/aletheia-spikelock`](locks/aletheia-spikelock) and [`locks/aletheia-bloomlock`](locks/aletheia-bloomlock). The file formats include EDF, BIDS-EEG, XDF, BrainVision, WFDB, and GDF.

## 移动机器人

![地图这一步只亮了两格。NetworkX 把空地图的地点个数记成 0，有路时一次就算到 3。这里在什么都没看见时停下来。看得到的时候，走一步是 2，走到头是 3。](docs/figures/robot-delta.png)

地上有三格。机器人这一步只“看见”了第一格，所以亮两格：它站着的地方，和正前方那一格。第三格要再走一步才到。图上绿色是这一步已经到的，橙色框是还没到的。

[NetworkX](https://github.com/networkx/networkx) 3.6.1 拿到一张完全空的图，地点个数是 0。路上有三格时，它一次就把能到的地方都算完，直接得到 3。0 会让后面的导航以为“没有地点，地板是空的”。一次得到 3，又把“还要再走一步”抹掉了。

我们把这两件事分开。路上还有格子、这一步却什么都没看见时，程序停下来。看得到第一格时，走一步是 **2**，走到头是 **3**。

一张更大的固定地图也是这样。256 个地点，8 个已经看见的起点，512 条单向的路，种子 `20260919`。走一步，到达 **24** 个地点。一直走到不能再走，到达 **214** 个地点。再跑一遍，还是 214。把步数放到 256，也是 214。

代码在 [`tick.py`](tick.py)、[`datalog.py`](datalog.py)、[`occgrid.py`](occgrid.py)。地图文件是仓库里的 `resources/synthetic/world.yaml`。

There are three tiles. On this step the robot has only “seen” the first one, so two tiles light up: where it stands, and the tile directly ahead. The third tile waits for another step. Green is reached on this step. The orange outline is not reached yet.

[NetworkX](https://github.com/networkx/networkx) 3.6.1, given a completely empty graph, reports 0 places. Given the three-tile path, it finishes every reachable place in one call and returns 3. A 0 tells the navigator “there are no places, the floor is clear.” A single 3 erases the fact that the last tile is still one step away.

We keep those apart. If the path is still there and this step saw nothing, the program stops. If the first tile was seen, one step reaches **2** and walking to the end reaches **3**.

A larger fixed map does the same thing. 256 places, 8 places already seen, 512 one-way roads, seed `20260919`. One step reaches **24** places. Walking until nothing new can be reached gets **214**. A second walk is 214 again. Allowing 256 steps is also 214.

The code is in [`tick.py`](tick.py), [`datalog.py`](datalog.py), and [`occgrid.py`](occgrid.py). The map file is `resources/synthetic/world.yaml`.

## 车

![雷达这一帧是空的。NumPy 把空雷达的长度算成 0.0，FilterPy 接受一次空更新并把位置留在 0.0。这里停下来报错。真有回波时，两个点仍算作 1，三次观测仍算作 3。](docs/figures/vehicle-delta.png)

车顶的雷达转一圈，应该得到一些回波点。图上实线是真有回波的方向，虚线是这一帧什么都没回来。

[NumPy](https://github.com/numpy/numpy) 2.4.6 对一帧一个点都没有的雷达求长度，得到 `0.0`。长度 0 看起来像“扫过了，周围是空的”。[FilterPy](https://github.com/rlabbe/filterpy) 1.4.5 做位置更新。我们交给它一次空更新，它接受了，估计位置留在 `0.0`。位置 0 看起来像“车在原点”，而不是“这一次没有观测”。

同一帧空雷达、同一次空观测，我们停下来。两个真实的雷达点仍算作 **1**。三次真实观测仍算作 **3**。

路网也一样。NetworkX 对一张没有节点的路图报告地点个数是 0。一条还没给出站点的游览路线，我们停下来。

代码在 [`locks/aletheia-voxelock`](locks/aletheia-voxelock)、[`locks/aletheia-kalmanlock`](locks/aletheia-kalmanlock)、[`locks/aletheia-tourlock`](locks/aletheia-tourlock)。

The roof lidar spins and should return some points. Solid rays in the picture are real returns. Dashed rays are a frame where nothing came back.

[NumPy](https://github.com/numpy/numpy) 2.4.6 measures the length of a lidar frame with no points and returns `0.0`. A length of 0 looks like “we scanned, and the surroundings are empty.” [FilterPy](https://github.com/rlabbe/filterpy) 1.4.5 updates a position. Given an empty update, it accepts it, and the estimated position stays at `0.0`. A position of 0 looks like “the car is at the origin,” which is different from “this update had no observation.”

On that same empty frame and that same empty update, we stop. Two real lidar points still count as **1**. Three real observations still count as **3**.

A road map does the same thing. NetworkX reports 0 places for a road graph with no nodes. A tour that has not named its stops makes us stop.

The code is in [`locks/aletheia-voxelock`](locks/aletheia-voxelock), [`locks/aletheia-kalmanlock`](locks/aletheia-kalmanlock), and [`locks/aletheia-tourlock`](locks/aletheia-tourlock).

## 规划时只看眼前，和看下一步，可以选出不同的动作

有一张奖励表。每一行是一个状态，每一列是一个动作，格子里是立刻能拿到的分数。

只看第 0 行里最大的那一格，叫贪心。它不管这个动作会把你带到哪个更差的状态。我们另外做了一次整数上的策略迭代：动作会把状态推进到下一格，下一格的分数打九折后再加回来。

一张两行的小表上，贪心选动作 **0**，因为它眼前的分数是 10。看下一步之后，选动作 **1**，因为动作 0 会走进一个分数是 −100 的状态。

一张更大的表有 256 个状态、8 个动作，种子同样是 `20260919`。贪心选 **2**。迭代选 **5**。再算一遍，还是 5。奖励表本身是空的时候，我们停下来，不写出动作 0。

There is a reward table. Each row is a state, each column is an action, and the cell is the score you get immediately.

Looking only at the biggest cell in row 0 is the greedy choice. It does not ask which worse state that action leads to. We also run policy iteration in integers: an action moves you to the next state, and that next state's score is added back after a 10% discount.

On a two-row table, greedy picks action **0** because the immediate score is 10. After looking ahead, the choice is action **1**, because action 0 steps into a state scored −100.

A larger table has 256 states and 8 actions, with the same seed `20260919`. Greedy picks **2**. Iteration picks **5**. A second run is 5 again. When the reward table itself is empty, we stop, and we do not write down action 0.

## 这些文件格式，空文件也按同一条规则处理

机器人栈已经在写这些文件。[ROS 的 map_server](https://wiki.ros.org/map_server) 用 YAML 加一张 PGM 图。[Foxglove 的 MCAP](https://github.com/foxglove/mcap) 是一条日志。[ROS 2 的 rosbag2](https://github.com/ros2/rosbag2) 是一个带 sqlite 数据库的文件夹。空白的格子图、零条消息的 MCAP、零条消息的 bag，我们都停下来。NetworkX 在那张三节点的图上，空图的节点列表是空的；边还在、这一步却没有起点时，我们停下来。

Robot stacks already write these files. [ROS map_server](https://wiki.ros.org/map_server) uses YAML plus a PGM image. [Foxglove MCAP](https://github.com/foxglove/mcap) is a log. [ROS 2 rosbag2](https://github.com/ros2/rosbag2) is a folder with a sqlite database. A blank grid, an MCAP with zero messages, and a bag with zero messages all make us stop. On the three-node picture, NetworkX's empty graph has an empty node list. When the edges are still there and this step has no starting place, we stop.

## 这些数是怎么来的

地图那一组来自 `results/TICK_EVIDENCE.json` 和 `results/DATALOG_EVIDENCE.json`。同一张地图用两种走法各算一次，走到头的人数应该一样，也和一次普通的广度优先搜索一样。

The map numbers come from `results/TICK_EVIDENCE.json` and `results/DATALOG_EVIDENCE.json`. Two walks to the end of the same map should match, and they should match an ordinary breadth-first search.

| 你看到的 | 意思 | 数 |
|---|---|---|
| 种子 | 随机地图用的固定种子，换一台机器也是这张图 | 20260919 |
| 地点 / 起点 / 路 | 256 个地点，8 个已经看见的起点，512 条单向路 | 256 / 8 / 512 |
| 走一步 | 只沿路走一格，新到达的地点个数 | 24 |
| 走到头，两遍 | 一直走到没有新地点，连做两遍 | 214 和 214 |
| 步数放到 256 | 步数够走到头 | 214 |
| 广度优先搜索 | 同一种“走到头”，用另一段代码算 | 214 |

奖励表那一组来自 `results/POLICY_EVIDENCE.json` 和 `results/SHOW_POLICY.json`。

The reward-table numbers come from `results/POLICY_EVIDENCE.json` and `results/SHOW_POLICY.json`.

| 你看到的 | 意思 | 数 |
|---|---|---|
| 两行小表 | 只看眼前 / 看下一步 | 动作 0 / 动作 1 |
| 256×8 的表 | 只看眼前 | 动作 2 |
| 同一张表再算一遍 | 看下一步，两遍 | 动作 5 和 5 |

时间也记在那两个 JSON 里。这张 256 个地点的地图上，走到头的中位时间大约 0.00031 秒，广度优先搜索大约 0.00013 秒。256×8 的奖励表上，看下一步的中位时间大约 0.0060 秒，只看眼前大约 0.000010 秒。这里比的是答案是否相同，不是谁更快。

The timings are in those same JSON files. On the 256-place map, walking to the end takes about 0.00031 seconds at the median, and breadth-first search about 0.00013 seconds. On the 256×8 reward table, looking ahead takes about 0.0060 seconds at the median, and looking only at the current row about 0.000010 seconds. The comparison is whether the answers agree, not which call is faster.

## 相关的开源项目

下表是我们并排调用过、或直接读取其文件的上游项目。链接指向他们自己的仓库。

The table is the upstream projects we call side by side, or whose files we read. Each link goes to their repository.

| 项目 | 地址 | 它是做什么的，我们拿它比了什么 |
|---|---|---|
| NetworkX | https://github.com/networkx/networkx | 图算法库。空图的地点个数是 0；三格的路它一次走到头。 |
| Foxglove MCAP | https://github.com/foxglove/mcap | 机器人日志格式。零条消息的日志，我们停下来。 |
| ROS 2 rosbag2 | https://github.com/ros2/rosbag2 | ROS 2 的数据包。零条消息的包，我们停下来。 |
| rosbags | https://gitlab.com/ternaris/rosbags | 用 Python 读 rosbag2 的库。`show_rosbags.py` 用的就是它。 |
| ROS map_server | https://wiki.ros.org/map_server | 用地图图片做导航的那一套。我们读它的 YAML 和 PGM。 |
| OccupancyGrid | https://docs.ros.org/en/humble/p/nav_msgs/interfaces/msg/OccupancyGrid.html | ROS 里“这一格有没有东西”的消息。空白格子图会让我们停下来。 |
| ROS 2 | https://github.com/ros2/ros2 | 上面这些包和地图所在的机器人系统。 |
| Soufflé | https://github.com/souffle-lang/souffle | 把“沿规则一直推到不能再推”做成系统的 Datalog 编译器。我们这份仓库里的走到头，是同一类推法，用在一张固定的地图上。 |
| NumPy | https://github.com/numpy/numpy | 数值库。空数组的平均值是 nan，空向量的长度是 0.0。 |
| MNE-Python | https://github.com/mne-tools/mne-python | 读脑电的库。空录音的时长是 0。 |
| BIDS | https://github.com/bids-standard/bids-specification | 脑电实验的文件约定。只有表头、没有事件的那份表，我们停下来。 |
| NiBabel | https://github.com/nipy/nibabel | 读医学影像 NIfTI。名字出现在格式索引里。 |
| OpenDRIVE | https://github.com/asam-oss/asamOpenDRIVE | 路和路口的地图格式。空的路口图，我们停下来。 |
| MuJoCo | https://github.com/google-deepmind/mujoco | 机器人仿真。空的手部模型会被加载成功。 |
| Open3D | https://github.com/isl-org/Open3D | 点云库。和雷达那一帧放在一起看。 |
| nuScenes | https://github.com/nutonomy/nuscenes-devkit | 自动驾驶数据集的读取工具。空样本会让我们停下来。 |
| pyahocorasick | https://github.com/WojciechMula/pyahocorasick | 字符串匹配。空文本和我们的后缀链接放在一起看。 |
| python-bloomfilter | https://github.com/joseph-fox/python-bloomfilter | Bloom 过滤器。没有键的过滤器会回答“不是成员”。 |

## 自己跑一遍

精度检查只用 Python 标准库。要看和 NetworkX、MCAP、rosbags 的并排结果，先装 `requirements-show.txt` 里钉住的版本。

The precision check uses the Python standard library only. To rerun the side-by-side calls against NetworkX, MCAP, and rosbags, install the versions pinned in `requirements-show.txt`.

```bash
make check
python3.12 show_tick.py
python3.12 show_policy.py
python3.12 show_networkx.py
```

`make check` 会重算上面那些该相等的数。每次推送到 GitHub 也会跑同样的检查。某一条对不上，命令会以非零状态退出。

`make check` recomputes the numbers that are supposed to match. The same check runs on every push to GitHub. If one of them moves, the command exits with a non-zero status.

## 仓库里还有什么

| 路径 | 它做什么 |
|---|---|
| `tick.py` | 只走一步。 |
| `datalog.py` | 走到不能再走。 |
| `policy.py` | 看下一步再选动作。空的奖励表会停下来。 |
| `occgrid.py` | 读 ROS 的格子地图，连成上下左右相邻的图。 |
| `mcapocc.py` | 读 MCAP 日志里的占据采样。 |
| `bagocc.py` | 读 rosbag2 文件夹。 |
| `tests/test_precision.py` | 上面这些该相等的数。 |
| `results/` | 已经跑出来的 JSON。 |
| `locks/` | 66 个小程序。每个认一种现成文件：脑电、雷达、手部模型、路口图，诸如此类。 |
| `binds/` | 100 本小登记册。一条记录没有名字时，不往同一个未命名的列表里追加。 |
| [`ATLAS.md`](ATLAS.md) | 上面两部分的目录。 |

`docs-awesome/` 里是 10 份公开的资源清单，`tools/` 里是 6 个小工具。这些计算不靠一份训练出来的权重，也没有梯度步。

`docs-awesome/` holds 10 public resource lists, and `tools/` holds 6 small tools. These calculations do not depend on a trained weight file, and they take no gradient steps.

## License / 许可

MIT
