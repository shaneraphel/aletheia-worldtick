#!/usr/bin/env python3.12
"""Show: a rosbag2 folder (an empty bag)."""
from __future__ import annotations
import json, platform, sqlite3, sys
from pathlib import Path
from bagocc import read_rosbag2, rosbag2_occupancy
from kalman import kalman_filter

BAG = Path(__file__).resolve().parent / "resources" / "synthetic" / "imu.bag"


def main():
    samples = read_rosbag2(BAG)
    steps = [(int(v), 0) for v in samples]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-imu.bag")
    p.mkdir(parents=True, exist_ok=True)
    (p / "metadata.yaml").write_text("rosbag2_bagfile_information:\n  storage_identifier: sqlite3\n")
    db = p / "bag_0.db3"
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    con.execute(
        "CREATE TABLE messages(id INTEGER PRIMARY KEY, topic_id INTEGER NOT NULL, "
        "timestamp INTEGER NOT NULL, data BLOB NOT NULL)"
    )
    con.commit()
    con.close()
    try:
        read_rosbag2(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "kalmanlock.show_rosbag2.v1",
        "used": "https://github.com/ros2/rosbag2",
        "built": "three rosbag2 samples, occupancy 3; empty bag is absence",
        "ours": {"n": rosbag2_occupancy(BAG), "kalman": kalman_filter(steps), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["kalman"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("kalmanlock rosbag2 show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
