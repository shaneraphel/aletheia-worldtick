"""MCAP occupancy. An empty log is absence, not 0 messages.

Foxglove / ROS 2 MCAP stores one occupancy sample per message. Zero
messages refuse. The writer uses the public mcap package so the tape
is a real log.
"""
from __future__ import annotations

from pathlib import Path

Z = -1


def write_mcap(path, samples):
    if samples is None or not samples:
        raise ValueError("uncompiled MCAP log is absence")
    from mcap.writer import Writer

    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as fh:
        w = Writer(fh)
        w.start(profile="aletheia", library="aletheia-mcapocc")
        sid = w.register_schema(name="occupancy", encoding="raw", data=b"")
        cid = w.register_channel(topic="/occupancy", message_encoding="raw", schema_id=sid)
        for i, x in enumerate(samples):
            w.add_message(
                channel_id=cid,
                log_time=i,
                publish_time=i,
                data=int(x).to_bytes(8, "little", signed=True),
                sequence=i,
            )
        w.finish()
    return dest


def read_mcap(path):
    dest = Path(path)
    if not dest.exists() or dest.stat().st_size < 16:
        raise ValueError("uncompiled MCAP log is absence")
    from mcap.reader import make_reader

    samples = []
    with dest.open("rb") as fh:
        for _schema, _channel, message in make_reader(fh).iter_messages():
            if not message.data:
                raise ValueError("uncompiled MCAP log is absence")
            samples.append(int.from_bytes(message.data[:8], "little", signed=True))
    if not samples:
        raise ValueError("uncompiled MCAP log is absence")
    return samples


def mcap_occupancy(path):
    return len(read_mcap(path))
