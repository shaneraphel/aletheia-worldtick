"""Eximia occupancy. An empty recording is absence, not 0 samples.

eXimia `.nxe` is 64 channels of multiplexed int16, Cz carries the tape.
Official MNE `read_raw_eximia` reads those samples at 1450 Hz. An empty
sample list refuses. Eximia has no comment channel; Persyst `.lay` and
Nihon Kohden `.LOG` and EyeLink MSG keep `trial_type` text.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1
N_CHAN = 64
CZ_INDEX = 32
SFREQ = 1450.0


def write_eximia(path, samples):
    if samples is None or not samples:
        raise ValueError("uncompiled Eximia recording is absence")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = bytearray()
    for x in samples:
        row = [0] * N_CHAN
        row[CZ_INDEX] = int(x)
        buf += struct.pack("<" + "h" * N_CHAN, *row)
    path.write_bytes(bytes(buf))
    return path


def read_eximia(path):
    path = Path(path)
    raw = path.read_bytes()
    frame = N_CHAN * 2
    if len(raw) < frame or len(raw) % frame != 0:
        raise ValueError("uncompiled Eximia recording is absence")
    n = len(raw) // frame
    if n < 1:
        raise ValueError("uncompiled Eximia recording is absence")
    samples = [
        struct.unpack_from("<h", raw, i * frame + CZ_INDEX * 2)[0] for i in range(n)
    ]
    return {"n_samples": n, "samples": samples}


def eximia_occupancy(path):
    return read_eximia(path)["n_samples"]
