# Worldtick · 世界一步

[![check](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml/badge.svg)](https://github.com/shaneraphel/aletheia-worldtick/actions/workflows/check.yml)

同一份输入上的结果。空记录报错。有内容的记录给出下面的数。

Same input, the result. An empty record reports an error. A record with contents gives the number below.

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
