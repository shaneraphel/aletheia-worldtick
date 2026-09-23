# Shows

Each script prints one JSON record and exits non-zero if its identity moves.

| command | what a reviewer sees |
|---|---|
| `python3.12 show_tick.py` | checked-in 1×3 map: one tick is 2, closure is 3 |
| `python3.12 show_policy.py` | greedy action 0, iterated action 1, empty table raises |
| `python3.12 show_networkx.py` | NetworkX 3.6.1 on the same 3-node world |
| `python3.12 show_occgrid.py` | ROS occupancy grid |
| `python3.12 show_mcap.py` | Foxglove MCAP |
| `python3.12 show_rosbag2.py` | rosbag2 folder |
| `python3.12 show_rosbags.py` | read through the `rosbags` package |

Pinned output lives in `results/`.
