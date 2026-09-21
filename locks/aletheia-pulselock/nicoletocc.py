"""Nicolet occupancy. An empty recording is absence, not 0 channels.

Nicolet stores a `.head` of `key=value` lines beside a `.data` of int16
samples. Official MNE `read_raw_nicolet` reads that pair. An empty sample
list refuses. Nicolet has no comment channel; Persyst `.lay` keeps
`trial_type` text.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1


def _pair(path):
    p = Path(path)
    if p.suffix == ".head":
        return p.with_suffix(".data"), p
    if p.suffix == ".data":
        return p, p.with_suffix(".head")
    return p.with_suffix(".data"), p.with_suffix(".head")


def write_nicolet(stem, samples, *, label="Cz"):
    if samples is None or not samples:
        raise ValueError("uncompiled Nicolet recording is absence")
    data, head = _pair(stem)
    data.parent.mkdir(parents=True, exist_ok=True)
    n = len(samples)
    data.write_bytes(b"".join(struct.pack("<h", int(x)) for x in samples))
    head.write_text(
        "\n".join(
            [
                f"elec_names=[{label}]",
                "sample_freq=1",
                "conversion_factor=1",
                "num_channels=1",
                f"num_samples={n}",
                "rec_id=1",
                "adm_id=1",
                "pat_id=1",
                "start_ts=2026-09-20 14:00:00.000000",
                "",
            ]
        )
    )
    return data


def read_nicolet(path):
    data, head = _pair(path)
    if not data.exists() or not head.exists():
        raise ValueError("uncompiled Nicolet recording is absence")
    raw = data.read_bytes()
    if len(raw) < 2:
        raise ValueError("uncompiled Nicolet recording is absence")
    samples = [struct.unpack_from("<h", raw, 2 * i)[0] for i in range(len(raw) // 2)]
    if not samples:
        raise ValueError("uncompiled Nicolet recording is absence")
    return {"n_samples": len(samples), "samples": samples}


def nicolet_occupancy(path):
    return read_nicolet(path)["n_samples"]
