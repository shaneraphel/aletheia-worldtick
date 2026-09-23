# What a world-tick resource is

One tick moves occupied facts across one edge. The closure is a later number.
On `resources/synthetic/world.yaml` those numbers are 2 and 3.

This kernel ingests a ROS OccupancyGrid (`resources/synthetic/world.yaml`).
A blank map refuses. Unknown and free cells are not facts.

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
python3.12 show_rosbags.py
```
