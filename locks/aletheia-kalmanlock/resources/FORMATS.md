# What an IMU resource is

KITTI raw OXTS is one pose/IMU row per sample. Zero rows refuse.

```bash
python3.12 show_oxts.py
```

ROS 2 rosbag2 is a folder of `metadata.yaml` plus sqlite3. Zero messages refuse.

```bash
python3.12 show_rosbag2.py
```
