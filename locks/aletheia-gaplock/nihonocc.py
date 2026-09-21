"""Nihon Kohden occupancy. An empty recording is absence, not 0 channels.

Nihon Kohden stores an `.EEG` waveform, a `.PNT` clock, and a `.LOG` of
trial labels. Official MNE `read_raw_nihon` copies LOG text into annotation
descriptions. An empty sample list or empty log list refuses. Channel index
is C3 so MNE does not treat `Z` in `CZ` as misc.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1
VER = b"EEG-1100A V01.00"
CTL = 0x1800
DATA = 0x1840
CH_C3 = 4
N_CH = 1
LOG_BLK = 0x100


def _stem(path):
    p = Path(path)
    if p.suffix.lower() in {".eeg", ".pnt", ".log"}:
        return p.with_suffix("")
    return p


def _norm_events(events):
    if events is not None and not events:
        raise ValueError("uncompiled Nihon Kohden recording is absence")
    if events is None:
        events = [(1.0, "go"), (2.0, "end")]
    rows = []
    for i, item in enumerate(events):
        if isinstance(item, str):
            onset, text = float(i + 1), item
        elif len(item) >= 2:
            onset, text = float(item[0]), str(item[1])
        else:
            raise ValueError("uncompiled Nihon Kohden recording is absence")
        if not text or not text.isascii() or len(text) > 20:
            raise ValueError("uncompiled Nihon Kohden recording is absence")
        sec = int(onset)
        if sec < 0 or sec > 86399:
            raise ValueError("uncompiled Nihon Kohden recording is absence")
        rows.append((sec, text))
    if not rows:
        raise ValueError("uncompiled Nihon Kohden recording is absence")
    return rows


def write_nihon(path, samples, events=None):
    if samples is None or not samples:
        raise ValueError("uncompiled Nihon Kohden recording is absence")
    if events is not None and not events:
        raise ValueError("uncompiled Nihon Kohden recording is absence")
    stem = _stem(path)
    stem.parent.mkdir(parents=True, exist_ok=True)
    n = len(samples)
    sfreq = 1
    duration = n * 10 // sfreq
    datastart = DATA + 0x27 + N_CH * 10
    size = datastart + n * (N_CH + 1) * 2
    buf = bytearray(size)
    buf[0:16] = VER
    buf[0x0081 : 0x0081 + 16] = VER
    buf[0x0091] = 1
    struct.pack_into("<I", buf, 0x0092, CTL)
    buf[0x17FE] = 1
    buf[CTL + 17] = 1
    struct.pack_into("<I", buf, CTL + 18, DATA)
    struct.pack_into("<H", buf, DATA + 0x1A, sfreq)
    struct.pack_into("<I", buf, DATA + 0x1C, duration)
    buf[DATA + 0x26] = N_CH
    buf[DATA + 0x27] = CH_C3
    off = datastart
    for x in samples:
        struct.pack_into("<H", buf, off, (int(x) + 0x8000) & 0xFFFF)
        off += 2
        struct.pack_into("<H", buf, off, 0x8000)
        off += 2
    stem.with_suffix(".EEG").write_bytes(bytes(buf))
    pnt = bytearray(0x50)
    pnt[0:16] = VER
    pnt[0x40 : 0x40 + 14] = b"20260920000000"
    stem.with_suffix(".PNT").write_bytes(bytes(pnt))
    rows = _norm_events(events)
    log_size = LOG_BLK + 0x14 + 45 * len(rows)
    log = bytearray(log_size)
    log[0:16] = VER
    log[0x91] = 1
    struct.pack_into("<I", log, 0x92, LOG_BLK)
    log[LOG_BLK + 0x12] = len(rows)
    for i, (sec, text) in enumerate(rows):
        base = LOG_BLK + 0x14 + i * 45
        raw = text.encode("ascii")
        log[base : base + 20] = raw + b"\x00" * (20 - len(raw))
        hms = f"{sec // 3600:02d}{(sec // 60) % 60:02d}{sec % 60:02d}"
        log[base + 20 : base + 26] = hms.encode("ascii")
    stem.with_suffix(".LOG").write_bytes(bytes(log))
    return stem.with_suffix(".EEG")


def read_nihon(path):
    eeg = _stem(path).with_suffix(".EEG")
    raw = eeg.read_bytes()
    if len(raw) < DATA + 0x28 or raw[0:16] != VER:
        raise ValueError("uncompiled Nihon Kohden recording is absence")
    nch = raw[DATA + 0x26]
    duration = struct.unpack_from("<I", raw, DATA + 0x1C)[0]
    sfreq = struct.unpack_from("<H", raw, DATA + 0x1A)[0] & 0x3FFF
    n = duration * sfreq // 10
    start = DATA + 0x27 + nch * 10
    need = start + n * (nch + 1) * 2
    if n < 1 or nch < 1 or len(raw) < need:
        raise ValueError("uncompiled Nihon Kohden recording is absence")
    samples = []
    for i in range(n):
        stored = struct.unpack_from("<H", raw, start + i * (nch + 1) * 2)[0]
        samples.append(stored - 0x8000)
    return {"n_samples": n, "samples": samples}


def read_nihon_log(path):
    log = _stem(path).with_suffix(".LOG")
    if not log.exists():
        raise ValueError("uncompiled Nihon Kohden recording is absence")
    raw = log.read_bytes()
    if len(raw) < LOG_BLK + 0x14 or raw[0:16] != VER:
        raise ValueError("uncompiled Nihon Kohden recording is absence")
    n_logs = raw[LOG_BLK + 0x12]
    texts = []
    for i in range(n_logs):
        base = LOG_BLK + 0x14 + i * 45
        if len(raw) < base + 26:
            raise ValueError("uncompiled Nihon Kohden recording is absence")
        text = raw[base : base + 20].split(b"\x00", 1)[0].decode("ascii")
        if text:
            texts.append(text)
    if not texts:
        raise ValueError("uncompiled Nihon Kohden recording is absence")
    return texts


def nihon_occupancy(path):
    return read_nihon(path)["n_samples"]
