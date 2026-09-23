#!/usr/bin/env python3.12
"""Show: a rosbag2 folder (an empty bag)."""
from __future__ import annotations
import json, platform, sqlite3, sys
from pathlib import Path
from bagocc import read_rosbag2, rosbag2_occupancy, write_rosbag2
from datalog import datalog_fixpoint

BAG = Path(__file__).resolve().parent / "resources" / "synthetic" / "world.bag"


def theirs() -> dict:
    empty = Path("/tmp/aletheia-empty.bag")
    empty.mkdir(parents=True, exist_ok=True)
    db = empty / "bag_0.db3"
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
    n = list(con.execute("SELECT COUNT(*) FROM messages"))[0][0]
    con.close()
    return {"storage": "sqlite3", "empty_messages": int(n)}


def main():
    samples = read_rosbag2(BAG)
    n = len(samples)
    facts = [0]
    edges = [(i, i + 1) for i in range(n - 1)]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-read.bag")
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
        "schema": "worldtick.show_rosbag2.v1",
        "used": "https://github.com/ros2/rosbag2",
        "built": "three rosbag2 samples, world reach 3; empty bag is absence",
        "theirs": theirs(),
        "ours": {"n": rosbag2_occupancy(BAG), "reach": datalog_fixpoint(n, facts, edges), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["reach"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("worldtick rosbag2 show identity failed")
    if rec["theirs"]["empty_messages"] != 0:
        raise SystemExit("sqlite empty bag identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
