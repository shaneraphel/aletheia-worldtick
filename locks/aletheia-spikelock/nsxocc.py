"""Blackrock NSX occupancy. An empty recording is absence, not 0 channels.

Blackrock `.ns3` is NEURALCD 2.2: a 314-byte basic header, 66-byte extended
header per channel, then a data packet (`header=0x01`, uint32 timestamp,
uint32 n_points, int16 samples). Official MNE `read_raw_nsx` reads those
samples. An empty sample list refuses. Comments stay on Persyst `.lay`;
NSX annotations are acquisition skips, not `trial_type` text.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1
BASIC = 314
EXTENDED = 66
PACKET = 9


def write_nsx(path, samples, *, label="Cz"):
    if samples is None or not samples:
        raise ValueError("uncompiled NSX recording is absence")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    n = len(samples)
    nch = 1
    hdr = BASIC + EXTENDED * nch
    buf = bytearray(hdr)

    def poke(off: int, width: int, text: str) -> None:
        raw = text.encode("ascii")
        if len(raw) > width:
            raise ValueError("uncompiled NSX recording is absence")
        buf[off : off + width] = raw + b"\x00" * (width - len(raw))

    buf[0:8] = b"NEURALCD"
    buf[8] = 2
    buf[9] = 2
    struct.pack_into("<I", buf, 10, hdr)
    poke(14, 16, "1 S/s")
    poke(30, 256, "aletheia")
    struct.pack_into("<I", buf, 286, 1)
    struct.pack_into("<I", buf, 290, 1)
    struct.pack_into("<8H", buf, 294, 2026, 9, 7, 20, 14, 0, 0, 0)
    struct.pack_into("<I", buf, 310, nch)
    off = BASIC
    buf[off : off + 2] = b"CC"
    struct.pack_into("<H", buf, off + 2, 1)
    poke(off + 4, 16, label)
    buf[off + 20] = 1
    buf[off + 21] = 1
    struct.pack_into("<hhhh", buf, off + 22, -32768, 32767, -32768, 32767)
    poke(off + 30, 16, "uV")
    pkt = bytearray(PACKET + 2 * n * nch)
    pkt[0] = 1
    struct.pack_into("<I", pkt, 1, 0)
    struct.pack_into("<I", pkt, 5, n)
    for i, x in enumerate(samples):
        struct.pack_into("<h", pkt, PACKET + 2 * i, int(x))
    path.write_bytes(bytes(buf) + bytes(pkt))
    return path


def read_nsx(path):
    path = Path(path)
    raw = path.read_bytes()
    if len(raw) < BASIC + EXTENDED + PACKET + 2:
        raise ValueError("uncompiled NSX recording is absence")
    if raw[0:8] != b"NEURALCD":
        raise ValueError("uncompiled NSX recording is absence")
    hdr = struct.unpack_from("<I", raw, 10)[0]
    nch = struct.unpack_from("<I", raw, 310)[0]
    if nch < 1 or hdr != BASIC + EXTENDED * nch:
        raise ValueError("uncompiled NSX recording is absence")
    if raw[hdr] != 1:
        raise ValueError("uncompiled NSX recording is absence")
    n = struct.unpack_from("<I", raw, hdr + 5)[0]
    start = hdr + PACKET
    need = start + 2 * n * nch
    if n < 1 or len(raw) < need:
        raise ValueError("uncompiled NSX recording is absence")
    samples = [
        struct.unpack_from("<h", raw, start + 2 * i * nch)[0] for i in range(n)
    ]
    return {"n_samples": n, "samples": samples}


def nsx_occupancy(path):
    return read_nsx(path)["n_samples"]
