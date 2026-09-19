#!/usr/bin/env python3.12
"""Show: I used rosbags on a rosbag2 folder, and I refused an empty bag.

rosbag2_py is absent (no ROS 2). rosbags reads the same MIT folder.
"""
from __future__ import annotations
import importlib.metadata, json, platform, sqlite3, sys
from pathlib import Path
from bagocc import read_rosbag2, rosbag2_occupancy
from datalog import datalog_fixpoint
from rosbags.rosbag2 import Reader

BAG = Path(__file__).resolve().parent / "resources" / "synthetic" / "world.bag"


def main():
    samples = read_rosbag2(BAG)
    n = len(samples)
    facts = [0]
    edges = [(i, i + 1) for i in range(n - 1)]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-read.bag")
    p.mkdir(parents=True, exist_ok=True)
    (p / "metadata.yaml").write_text(
        "rosbag2_bagfile_information:\n"
        "  version: 5\n"
        "  storage_identifier: sqlite3\n"
        "  relative_file_paths:\n"
        "    - bag_0.db3\n"
        "  duration:\n"
        "    nanoseconds: 0\n"
        "  starting_time:\n"
        "    nanoseconds_since_epoch: 0\n"
        "  message_count: 0\n"
        "  topics_with_message_count: []\n"
    )
    db = p / "bag_0.db3"
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    con.execute(
        "CREATE TABLE topics(id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT NOT NULL, "
        "serialization_format TEXT NOT NULL, offered_qos_profiles TEXT NOT NULL)"
    )
    con.execute(
        "CREATE TABLE messages(id INTEGER PRIMARY KEY, topic_id INTEGER NOT NULL, "
        "timestamp INTEGER NOT NULL, data BLOB NOT NULL)"
    )
    con.commit()
    con.close()
    with Reader(str(p)) as r:
        theirs_empty = sum(1 for _ in r.messages())
    with Reader(str(BAG)) as r:
        theirs_n = int(r.message_count)
    try:
        read_rosbag2(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "worldtick.show_rosbags.v1",
        "used": "https://github.com/ternaris/rosbags",
        "rosbag2_py": "Z_named_not_installed",
        "built": "three rosbag2 samples, world reach 3; empty bag is absence",
        "theirs": {
            "package": "rosbags",
            "version": importlib.metadata.version("rosbags"),
            "empty_messages": theirs_empty,
            "bag_messages": theirs_n,
        },
        "ours": {"n": rosbag2_occupancy(BAG), "reach": datalog_fixpoint(n, facts, edges), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["reach"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("worldtick rosbags show identity failed")
    if rec["theirs"]["empty_messages"] != 0 or rec["theirs"]["bag_messages"] != 3:
        raise SystemExit("rosbags bag identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
