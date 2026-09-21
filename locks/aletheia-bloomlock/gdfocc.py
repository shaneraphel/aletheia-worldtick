"""GDF occupancy. An empty recording is absence, not 0 channels.

GDF 1.25 is the BioSig interchange MNE reads next to EDF. This writer emits
the 1.x header (256-byte fixed + field-major 256-byte signal + int16 +
mode-0 event byte). It is not a second BioSig 2.20 stack: no typed event
table, no impedance, no latitude. Zero channels, zero records, or zero
samples refuse.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1


def _pad(text: str, width: int) -> bytes:
    raw = text.encode("ascii", "replace")
    if len(raw) > width:
        raw = raw[:width]
    return raw + b" " * (width - len(raw))


def write_gdf(path, samples, *, label="EEG Cz", n_chan=1):
    if samples is None or not samples:
        raise ValueError("uncompiled GDF recording is absence")
    n_chan = int(n_chan)
    if n_chan < 1:
        raise ValueError("uncompiled GDF recording is absence")
    vals = [int(x) for x in samples]
    if n_chan == 1:
        n_samp = len(vals)
        per_chan = [vals]
    else:
        if len(vals) != n_chan:
            raise ValueError("uncompiled GDF recording is absence")
        n_samp = 1
        per_chan = [[v] for v in vals]
    if n_samp < 1:
        raise ValueError("uncompiled GDF recording is absence")
    header_nbytes = 256 + 256 * n_chan
    buf = bytearray()
    buf += _pad("GDF 1.25", 8)
    buf += _pad("X X X X", 80)
    buf += _pad("Startdate X X X", 80)
    buf += _pad("2026091923000000", 16)
    buf += struct.pack("<q", header_nbytes)
    buf += bytes(8)
    buf += bytes(8)
    buf += bytes(8)
    buf += bytes(20)
    buf += struct.pack("<q", 1)
    buf += struct.pack("<II", 1, 1)
    buf += struct.pack("<I", n_chan)
    if len(buf) != 256:
        raise ValueError("uncompiled GDF recording is absence")
    names = [label if n_chan == 1 else f"{label}{i}" for i in range(n_chan)]
    for name in names:
        buf += _pad(name, 16)
    for _ in range(n_chan):
        buf += _pad("AgAgCl cup", 80)
    for _ in range(n_chan):
        buf += _pad("uV", 8)
    for _ in range(n_chan):
        buf += struct.pack("<d", -32768.0)
    for _ in range(n_chan):
        buf += struct.pack("<d", 32767.0)
    for _ in range(n_chan):
        buf += struct.pack("<q", -32768)
    for _ in range(n_chan):
        buf += struct.pack("<q", 32767)
    for _ in range(n_chan):
        buf += _pad("HP:0.1Hz LP:40Hz", 80)
    for _ in range(n_chan):
        buf += struct.pack("<i", n_samp)
    for _ in range(n_chan):
        buf += struct.pack("<i", 3)
    for _ in range(n_chan):
        buf += bytes(32)
    if len(buf) != header_nbytes:
        raise ValueError("uncompiled GDF recording is absence")
    # one record: channels concatenated, each n_samp int16
    data = bytearray()
    for ch in per_chan:
        for x in ch:
            data += struct.pack("<h", int(x))
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    # GDF 1.x event table: mode 0 = no events. MNE still reads this byte.
    dest.write_bytes(bytes(buf) + bytes(data) + b"\x00")
    return dest


def write_gdf_word(path, word):
    if word is None or not str(word):
        raise ValueError("uncompiled GDF recording is absence")
    return write_gdf(path, [ord(c) for c in str(word)], label="EEG")


def write_gdf_sick(path, n, sick):
    if n is None or n < 1 or sick is None or not sick:
        raise ValueError("uncompiled GDF recording is absence")
    samples = [1 if i in set(int(x) for x in sick) else 0 for i in range(int(n))]
    if sum(samples) < 1:
        raise ValueError("uncompiled GDF recording is absence")
    return write_gdf(path, samples, label="EEG", n_chan=int(n))


def read_gdf(path):
    raw = Path(path).read_bytes() if not isinstance(path, (bytes, bytearray)) else bytes(path)
    if not raw or len(raw) < 256:
        raise ValueError("uncompiled GDF recording is absence")
    version = raw[0:8].decode("ascii", "replace")
    if not version.startswith("GDF"):
        raise ValueError("uncompiled GDF recording is absence")
    try:
        number = float(version[4:].strip() or "0")
    except ValueError as exc:
        raise ValueError("uncompiled GDF recording is absence") from exc
    if number >= 1.9:
        raise ValueError("uncompiled GDF recording is absence")
    n_records = struct.unpack_from("<q", raw, 236)[0]
    n_chan = struct.unpack_from("<I", raw, 252)[0]
    if n_records < 1 or n_chan < 1:
        raise ValueError("uncompiled GDF recording is absence")
    header_nbytes = 256 + 256 * n_chan
    if len(raw) < header_nbytes:
        raise ValueError("uncompiled GDF recording is absence")
    n_samp = struct.unpack_from("<i", raw, 256 + 216 * n_chan)[0]
    dtype = struct.unpack_from("<i", raw, 256 + 216 * n_chan + 4 * n_chan)[0]
    if n_samp < 1 or dtype != 3:
        raise ValueError("uncompiled GDF recording is absence")
    need = header_nbytes + 2 * n_samp * n_chan * n_records
    if len(raw) < need:
        raise ValueError("uncompiled GDF recording is absence")
    samples = [
        struct.unpack_from("<h", raw, header_nbytes + 2 * i)[0]
        for i in range(n_samp * n_chan * n_records)
    ]
    label = raw[256:272].decode("ascii", "replace").strip()
    return {
        "n_signals": n_chan,
        "n_samples": n_samp * n_records,
        "label": label,
        "samples": samples,
        "version": version.strip(),
    }


def read_gdf_word(path):
    rec = read_gdf(path)
    return "".join(chr(int(v)) for v in rec["samples"])


def read_gdf_sick(path):
    rec = read_gdf(path)
    n = rec["n_signals"]
    sick = [i for i, v in enumerate(rec["samples"][:n]) if int(v) != 0]
    if n < 1 or not sick:
        raise ValueError("uncompiled GDF recording is absence")
    return n, sick


def gdf_occupancy(path):
    rec = read_gdf(path)
    return rec["n_samples"] * rec["n_signals"]
