"""WFDB occupancy. An empty recording is absence, not 0 signals.

PhysioNet stores many EEG and ECG tapes as .hea + .dat. This writer emits
format 16 (16-bit two's complement, least significant byte first), one
signal. `write_wfdb_atr` emits MIT annotation words: NOTE plus aux_note
copies `trial_type`. Official wfdb `rdann` reads those notes. Zero
signals or an empty annotation list refuse.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1

NOTE = 22
SKIP = 59
AUX = 63


def write_wfdb(stem, samples, *, label="EEG_Cz", annotations=None):
    if samples is None or not samples:
        raise ValueError("uncompiled WFDB recording is absence")
    if annotations is not None and not annotations:
        raise ValueError("uncompiled WFDB recording is absence")
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    rec = stem.name
    hea = stem.with_suffix(".hea")
    dat = stem.with_suffix(".dat")
    n = len(samples)
    dat.write_bytes(b"".join(struct.pack("<h", int(x)) for x in samples))
    hea.write_text(f"{rec} 1 8 {n}\n{rec}.dat 16 200/uV 8 0 0 {samples[0]} 0 0 {label}\n")
    if annotations is not None:
        write_wfdb_atr(stem, annotations, fs=8.0)
    return hea


def _atr_path(path):
    dest = Path(path)
    if dest.suffix == ".atr":
        return dest
    return dest.with_suffix(".atr")


def _fs_from_hea(stem):
    hea = Path(stem).with_suffix(".hea")
    if not hea.exists():
        return 8.0
    rec = hea.read_text().splitlines()[0].split()
    if len(rec) < 3:
        return 8.0
    return float(rec[2])


def _norm_atr(annotations, fs):
    if annotations is not None and not annotations:
        raise ValueError("uncompiled WFDB recording is absence")
    if annotations is None:
        annotations = [(1.0, "go"), (2.0, "end")]
    rows = []
    for i, item in enumerate(annotations):
        if isinstance(item, str):
            onset, text = float(i + 1), item
        elif isinstance(item, dict):
            onset, text = float(item["onset"]), str(item["text"])
        elif len(item) >= 2:
            onset, text = float(item[0]), str(item[1])
        else:
            raise ValueError("uncompiled WFDB recording is absence")
        if not text or not text.isascii():
            raise ValueError("uncompiled WFDB recording is absence")
        rows.append((int(round(onset * fs)), text))
    if not rows:
        raise ValueError("uncompiled WFDB recording is absence")
    return rows


def _ann_word(sd, typecode):
    return bytes([sd & 255, ((sd & 768) >> 8) + 4 * typecode])


def _skip_bytes(n):
    return bytes(
        [
            0,
            SKIP << 2,
            (n >> 16) & 255,
            (n >> 24) & 255,
            n & 255,
            (n >> 8) & 255,
        ]
    )


def _aux_bytes(text):
    raw = text.encode("ascii")
    out = bytes([len(raw), AUX << 2]) + raw
    if len(raw) % 2:
        out += b"\x00"
    return out


def write_wfdb_atr(stem, annotations=None, *, fs=None):
    if annotations is not None and not annotations:
        raise ValueError("uncompiled WFDB recording is absence")
    dest = _atr_path(stem)
    dest.parent.mkdir(parents=True, exist_ok=True)
    rate = float(fs) if fs is not None else _fs_from_hea(stem)
    rows = _norm_atr(annotations, rate)
    blob = bytearray()
    prev = 0
    for sample, text in rows:
        sd = int(sample) - prev
        if sd < 0:
            raise ValueError("uncompiled WFDB recording is absence")
        while sd > 1023:
            n = min(sd, 0x7FFFFFFF)
            blob.extend(_skip_bytes(n))
            sd -= n
        blob.extend(_ann_word(sd, NOTE))
        blob.extend(_aux_bytes(text))
        prev = int(sample)
    blob.extend(b"\x00\x00")
    dest.write_bytes(bytes(blob))
    return dest


def read_wfdb(hea):
    p = Path(hea)
    if not p.exists():
        raise ValueError("uncompiled WFDB recording is absence")
    lines = [ln for ln in p.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    if not lines:
        raise ValueError("uncompiled WFDB recording is absence")
    rec = lines[0].split()
    if len(rec) < 2:
        raise ValueError("uncompiled WFDB recording is absence")
    n_sig = int(rec[1])
    if n_sig < 1:
        raise ValueError("uncompiled WFDB recording is absence")
    dat = p.with_suffix(".dat")
    if not dat.exists():
        raise ValueError("uncompiled WFDB recording is absence")
    raw = dat.read_bytes()
    if len(raw) < 2:
        raise ValueError("uncompiled WFDB recording is absence")
    samples = [struct.unpack_from("<h", raw, 2 * i)[0] for i in range(len(raw) // 2)]
    return {"n_signals": n_sig, "n_samples": len(samples), "samples": samples}


def read_wfdb_atr(path):
    dest = _atr_path(path)
    if not dest.exists() or dest.stat().st_size < 2:
        raise ValueError("uncompiled WFDB recording is absence")
    raw = dest.read_bytes()
    i = 0
    notes = []
    while i + 2 <= len(raw):
        lo, hi = raw[i], raw[i + 1]
        i += 2
        sd = lo + ((hi & 3) << 8)
        typ = hi >> 2
        if typ == 0 and sd == 0:
            break
        if typ == SKIP:
            if i + 4 > len(raw):
                raise ValueError("uncompiled WFDB recording is absence")
            i += 4
            continue
        while i + 2 <= len(raw):
            lo2, hi2 = raw[i], raw[i + 1]
            typ2 = hi2 >> 2
            if typ2 == AUX:
                n = lo2
                i += 2
                need = n + (n % 2)
                if i + need > len(raw):
                    raise ValueError("uncompiled WFDB recording is absence")
                notes.append(raw[i : i + n].decode("ascii"))
                i += need
            elif typ2 in (60, 61, 62):
                i += 2
            else:
                break
    if not notes:
        raise ValueError("uncompiled WFDB recording is absence")
    return notes


def wfdb_occupancy(hea):
    return read_wfdb(hea)["n_samples"]
