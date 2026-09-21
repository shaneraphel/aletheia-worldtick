"""rosbag2 occupancy. An empty bag is absence, not 0 messages.

ROS 2 records a folder of metadata.yaml plus sqlite3. Zero messages refuse.
Payload is little-endian int64 occupancy, not a rewritten CDR stack.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

Z = -1


def write_rosbag2(folder, samples, topic="/occupancy"):
    if samples is None or not samples:
        raise ValueError("uncompiled rosbag2 log is absence")
    dest = Path(folder)
    dest.mkdir(parents=True, exist_ok=True)
    db = dest / "bag_0.db3"
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    con.execute(
        "CREATE TABLE topics("
        "id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT NOT NULL, "
        "serialization_format TEXT NOT NULL, offered_qos_profiles TEXT NOT NULL)"
    )
    con.execute(
        "CREATE TABLE messages("
        "id INTEGER PRIMARY KEY, topic_id INTEGER NOT NULL, "
        "timestamp INTEGER NOT NULL, data BLOB NOT NULL)"
    )
    con.execute(
        "INSERT INTO topics VALUES (1, ?, 'aletheia/msg/Occupancy', 'cdr', '')",
        (topic,),
    )
    for i, x in enumerate(samples):
        con.execute(
            "INSERT INTO messages VALUES (NULL, 1, ?, ?)",
            (i, int(x).to_bytes(8, "little", signed=True)),
        )
    con.commit()
    con.close()
    n = len(samples)
    (dest / "metadata.yaml").write_text(
        "rosbag2_bagfile_information:\n"
        "  version: 5\n"
        "  storage_identifier: sqlite3\n"
        "  relative_file_paths:\n"
        "    - bag_0.db3\n"
        "  duration:\n"
        f"    nanoseconds: {max(0, n - 1)}\n"
        "  starting_time:\n"
        "    nanoseconds_since_epoch: 0\n"
        f"  message_count: {n}\n"
        "  topics_with_message_count:\n"
        "    - topic_metadata:\n"
        f"        name: {topic}\n"
        "        type: aletheia/msg/Occupancy\n"
        "        serialization_format: cdr\n"
        '        offered_qos_profiles: ""\n'
        f"      message_count: {n}\n"
        '  compression_format: ""\n'
        '  compression_mode: ""\n'
    )
    return dest


def read_rosbag2(folder):
    dest = Path(folder)
    meta = dest / "metadata.yaml"
    db = dest / "bag_0.db3"
    if not meta.exists() or not db.exists():
        raise ValueError("uncompiled rosbag2 log is absence")
    text = meta.read_text()
    if "rosbag2_bagfile_information" not in text or "sqlite3" not in text:
        raise ValueError("uncompiled rosbag2 log is absence")
    con = sqlite3.connect(db)
    rows = list(con.execute("SELECT data FROM messages ORDER BY timestamp, id"))
    con.close()
    if not rows:
        raise ValueError("uncompiled rosbag2 log is absence")
    samples = []
    for (blob,) in rows:
        if not blob:
            raise ValueError("uncompiled rosbag2 log is absence")
        samples.append(int.from_bytes(blob[:8], "little", signed=True))
    return samples


def rosbag2_occupancy(folder):
    return len(read_rosbag2(folder))
