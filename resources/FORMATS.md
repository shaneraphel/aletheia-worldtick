# What a world-model map resource is

This kernel **ingests** a ROS OccupancyGrid (`resources/synthetic/world.yaml`).
Empty facts refuse.

```bash
python3.12 show_occgrid.py
```

Foxglove MCAP stores one occupancy sample per message. Zero messages refuse.

```bash
python3.12 show_mcap.py
```

ROS 2 rosbag2 is a folder of `metadata.yaml` plus sqlite3. Zero messages refuse.

```bash
python3.12 show_rosbag2.py
```
