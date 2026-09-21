#!/usr/bin/env python3.12
"""Show: I used a rosbag2 folder, and I refused an empty bag."""
from __future__ import annotations
import json, platform, sqlite3, sys
from pathlib import Path
from bagocc import read_rosbag2, rosbag2_occupancy
from kstren import max_k_subarray_strength

BAG = Path(__file__).resolve().parent / "resources" / "synthetic" / "pulse.bag"


def theirs() -> dict:
    empty = Path("/tmp/aletheia-empty.bag")
    empty.mkdir(parents=True, exist_ok=True)
    db = empty / "bag_0.db3"
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    con.execute(
        "CREATE TABLE messages(id INTEGER PRIMARY KEY, topic_id INTEGER NOT NULL, "
        "timestamp INTEGER NOT NULL, data BLOB NOT NULL)"
    )
    con.commit()
    n = list(con.execute("SELECT COUNT(*) FROM messages"))[0][0]
    con.close()
    return {"storage": "sqlite3", "empty_messages": int(n)}


def main():
    nums = read_rosbag2(BAG)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-pulse.bag")
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
        "schema": "pulselock.show_rosbag2.v1",
        "used": "https://github.com/ros2/rosbag2",
        "built": "five rosbag2 samples, pulse strength 22; empty bag is absence",
        "theirs": theirs(),
        "ours": {"n": rosbag2_occupancy(BAG), "strength": max_k_subarray_strength(nums, 3), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["strength"] != 22 or rec["ours"]["empty"] != "raised":
        raise SystemExit("pulselock rosbag2 show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
