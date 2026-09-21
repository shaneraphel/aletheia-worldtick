"""EDF/BDF occupancy. An empty recording is absence, not 0 channels.

EDF is the PhysioNet / OpenNeuro interchange. This writer emits EDF 1.0
(256-byte file header + 256-byte signal header + little-endian int16
samples). With annotations it emits EDF+C plus an `EDF Annotations`
TAL channel. `write_bdf` emits Biosemi 24-bit BDF (`\\xffBIOSEMI`) and
BDF+C plus a `BDF Annotations` TAL channel. Official MNE and edfio read
those descriptions. An empty sample list or empty annotation list refuses.
"""
from __future__ import annotations

import re
import struct
from pathlib import Path

Z = -1

_TAL_RE = re.compile(rb"([+-]\d+\.?\d*)(\x15(\d+\.?\d*))?(\x14.*?)\x14\x00")


def _pad(text: str, width: int) -> bytes:
    raw = text.encode("ascii")
    if len(raw) > width:
        raise ValueError("uncompiled EDF field is absence")
    return raw + b" " * (width - len(raw))


def _ns_field(values, width: int) -> bytes:
    return b"".join(_pad(v, width) for v in values)


def _onset_text(onset: float) -> str:
    v = float(onset)
    if v.is_integer():
        return f"{int(v):+d}"
    return f"{v:+g}"


def _tal_bytes(annotations) -> bytes:
    parts = [b"+0\x14\x14\x00"]
    for i, item in enumerate(annotations):
        if item is None:
            raise ValueError("uncompiled EDF recording is absence")
        if isinstance(item, str):
            onset, text = float(i + 1), item
        elif len(item) >= 2:
            onset, text = float(item[0]), str(item[1])
        else:
            raise ValueError("uncompiled EDF recording is absence")
        if not text or not text.isascii() or "\x14" in text:
            raise ValueError("uncompiled EDF recording is absence")
        parts.append(f"{_onset_text(onset)}\x14{text}\x14\x00".encode("ascii"))
    return b"".join(parts)


def _tal_samples(blob: bytes, n_samp: int) -> list[int]:
    need = n_samp * 2
    if len(blob) > need:
        raise ValueError("uncompiled EDF recording is absence")
    raw = blob + b"\x00" * (need - len(blob))
    return [struct.unpack_from("<h", raw, 2 * i)[0] for i in range(n_samp)]


def _i24(value: int) -> bytes:
    v = int(value)
    if v < 0:
        v += 1 << 24
    return bytes([v & 255, (v >> 8) & 255, (v >> 16) & 255])


def _from_i24(raw: bytes, offset: int) -> int:
    v = raw[offset] | (raw[offset + 1] << 8) | (raw[offset + 2] << 16)
    if v >= 1 << 23:
        v -= 1 << 24
    return v


def _tal_samples_bdf(blob: bytes, n_samp: int) -> list[int]:
    need = n_samp * 3
    if len(blob) > need:
        raise ValueError("uncompiled BDF recording is absence")
    raw = blob + b"\x00" * (need - len(blob))
    return [_from_i24(raw, 3 * i) for i in range(n_samp)]


def write_bdf(path, samples, *, label="EEG Cz", annotations=None):
    if samples is None or not samples:
        raise ValueError("uncompiled BDF recording is absence")
    if annotations is not None and not annotations:
        raise ValueError("uncompiled BDF recording is absence")
    n_eeg = len(samples)
    n_rec = 1
    annots = list(annotations) if annotations is not None else None
    n_sig = 2 if annots is not None else 1
    reserved = "BDF+C" if annots is not None else ""
    rec_dur = str(max(n_eeg, 3)) if annots is not None else "1"
    header_bytes = 256 + 256 * n_sig
    labels = [label]
    transducers = ["AgAgCl cup"]
    dims = ["uV"]
    pmin = ["-8388608"]
    pmax = ["8388607"]
    dmin = ["-8388608"]
    dmax = ["8388607"]
    pre = ["HP:0.1Hz LP:40Hz"]
    nsamp = [str(n_eeg)]
    rsv = [""]
    tal_samps: list[int] = []
    if annots is not None:
        blob = _tal_bytes(annots)
        n_tal = max(16, (len(blob) + 2) // 3)
        tal_samps = _tal_samples_bdf(blob, n_tal)
        labels.append("BDF Annotations")
        transducers.append("")
        dims.append("")
        pmin.append("-8388608")
        pmax.append("8388607")
        dmin.append("-8388608")
        dmax.append("8388607")
        pre.append("")
        nsamp.append(str(n_tal))
        rsv.append("")
    hdr = b"".join(
        [
            b"\xffBIOSEMI",
            _pad("X X X X", 80),
            _pad("Startdate 19-SEP-2026 X X X", 80),
            _pad("19.09.26", 8),
            _pad("23.00.00", 8),
            _pad(str(header_bytes), 8),
            _pad(reserved, 44),
            _pad(str(n_rec), 8),
            _pad(rec_dur, 8),
            _pad(str(n_sig), 4),
        ]
    )
    sig = b"".join(
        [
            _ns_field(labels, 16),
            _ns_field(transducers, 80),
            _ns_field(dims, 8),
            _ns_field(pmin, 8),
            _ns_field(pmax, 8),
            _ns_field(dmin, 8),
            _ns_field(dmax, 8),
            _ns_field(pre, 80),
            _ns_field(nsamp, 8),
            _ns_field(rsv, 32),
        ]
    )
    data = b"".join(_i24(int(x)) for x in samples)
    if tal_samps:
        data += b"".join(_i24(int(x)) for x in tal_samps)
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(hdr + sig + data)
    return dest


def write_edf(path, samples, *, label="EEG Cz", annotations=None):
    if samples is None or not samples:
        raise ValueError("uncompiled EDF recording is absence")
    if annotations is not None and not annotations:
        raise ValueError("uncompiled EDF recording is absence")
    n_eeg = len(samples)
    n_rec = 1
    annots = list(annotations) if annotations is not None else None
    n_sig = 2 if annots is not None else 1
    reserved = "EDF+C" if annots is not None else ""
    rec_dur = str(max(n_eeg, 3)) if annots is not None else "1"
    header_bytes = 256 + 256 * n_sig
    labels = [label]
    transducers = ["AgAgCl cup"]
    dims = ["uV"]
    pmin = ["-100"]
    pmax = ["100"]
    dmin = ["-32768"]
    dmax = ["32767"]
    pre = ["HP:0.1Hz LP:40Hz"]
    nsamp = [str(n_eeg)]
    rsv = [""]
    tal_samps: list[int] = []
    if annots is not None:
        blob = _tal_bytes(annots)
        n_tal = max(16, (len(blob) + 1) // 2)
        tal_samps = _tal_samples(blob, n_tal)
        labels.append("EDF Annotations")
        transducers.append("")
        dims.append("")
        pmin.append("-32768")
        pmax.append("32767")
        dmin.append("-32768")
        dmax.append("32767")
        pre.append("")
        nsamp.append(str(n_tal))
        rsv.append("")
    hdr = b"".join(
        [
            _pad("0", 8),
            _pad("X X X X", 80),
            _pad("Startdate 19-SEP-2026 X X X", 80),
            _pad("19.09.26", 8),
            _pad("23.00.00", 8),
            _pad(str(header_bytes), 8),
            _pad(reserved, 44),
            _pad(str(n_rec), 8),
            _pad(rec_dur, 8),
            _pad(str(n_sig), 4),
        ]
    )
    sig = b"".join(
        [
            _ns_field(labels, 16),
            _ns_field(transducers, 80),
            _ns_field(dims, 8),
            _ns_field(pmin, 8),
            _ns_field(pmax, 8),
            _ns_field(dmin, 8),
            _ns_field(dmax, 8),
            _ns_field(pre, 80),
            _ns_field(nsamp, 8),
            _ns_field(rsv, 32),
        ]
    )
    data = b"".join(struct.pack("<h", int(x)) for x in samples)
    if tal_samps:
        data += b"".join(struct.pack("<h", int(x)) for x in tal_samps)
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(hdr + sig + data)
    return dest


def _parse_sig(raw: bytes, n_sig: int):
    i = 256

    def take(width: int):
        nonlocal i
        vals = [raw[i + j * width : i + (j + 1) * width].decode("ascii").strip() for j in range(n_sig)]
        i += width * n_sig
        return vals

    labels = take(16)
    take(80)
    take(8)
    take(8)
    take(8)
    take(8)
    take(8)
    take(80)
    nsamp = [int(x or "0") for x in take(8)]
    take(32)
    return labels, nsamp, i


def _parse_tal(digital) -> list[tuple[float, float, str]]:
    raw = b"".join(struct.pack("<h", int(x)) for x in digital)
    rows = []
    for ev in _TAL_RE.findall(raw):
        onset = float(ev[0])
        duration = float(ev[2]) if ev[2] else 0.0
        for desc in ev[3].split(b"\x14")[1:]:
            text = desc.decode("ascii")
            if text:
                rows.append((onset, duration, text))
    return rows


def read_edf(path):
    raw = Path(path).read_bytes() if not isinstance(path, (bytes, bytearray)) else bytes(path)
    if not raw or len(raw) < 256:
        raise ValueError("uncompiled EDF recording is absence")
    n_sig = int(raw[252:256].decode("ascii").strip() or "0")
    if n_sig < 1:
        raise ValueError("uncompiled EDF recording is absence")
    n_rec = int(raw[236:244].decode("ascii").strip() or "0")
    if n_rec < 1:
        raise ValueError("uncompiled EDF recording is absence")
    if len(raw) < 256 + 256 * n_sig:
        raise ValueError("uncompiled EDF recording is absence")
    labels, nsamp, start = _parse_sig(raw, n_sig)
    if any(n < 1 for n in nsamp):
        raise ValueError("uncompiled EDF recording is absence")
    rec_bytes = sum(2 * n for n in nsamp)
    need = start + rec_bytes * n_rec
    if len(raw) < need:
        raise ValueError("uncompiled EDF recording is absence")
    eeg_i = next((i for i, lab in enumerate(labels) if lab != "EDF Annotations"), None)
    if eeg_i is None:
        raise ValueError("uncompiled EDF recording is absence")
    tal_i = next((i for i, lab in enumerate(labels) if lab == "EDF Annotations"), None)
    off_eeg = sum(2 * nsamp[k] for k in range(eeg_i))
    samples = []
    tal_digital = []
    for rec in range(n_rec):
        base = start + rec * rec_bytes
        for j in range(nsamp[eeg_i]):
            samples.append(struct.unpack_from("<h", raw, base + off_eeg + 2 * j)[0])
        if tal_i is not None:
            off_tal = sum(2 * nsamp[k] for k in range(tal_i))
            for j in range(nsamp[tal_i]):
                tal_digital.append(struct.unpack_from("<h", raw, base + off_tal + 2 * j)[0])
    annotations = _parse_tal(tal_digital) if tal_i is not None else []
    return {
        "n_signals": 1,
        "n_samples": len(samples),
        "label": labels[eeg_i],
        "samples": samples,
        "annotations": annotations,
    }


def read_edf_annotations(path):
    rec = read_edf(path)
    texts = [row[2] for row in rec["annotations"]]
    if not texts:
        raise ValueError("uncompiled EDF recording is absence")
    return texts


def read_bdf(path):
    raw = Path(path).read_bytes() if not isinstance(path, (bytes, bytearray)) else bytes(path)
    if not raw or len(raw) < 256 or raw[:8] != b"\xffBIOSEMI":
        raise ValueError("uncompiled BDF recording is absence")
    n_sig = int(raw[252:256].decode("ascii").strip() or "0")
    if n_sig < 1:
        raise ValueError("uncompiled BDF recording is absence")
    n_rec = int(raw[236:244].decode("ascii").strip() or "0")
    if n_rec < 1:
        raise ValueError("uncompiled BDF recording is absence")
    if len(raw) < 256 + 256 * n_sig:
        raise ValueError("uncompiled BDF recording is absence")
    labels, nsamp, start = _parse_sig(raw, n_sig)
    if any(n < 1 for n in nsamp):
        raise ValueError("uncompiled BDF recording is absence")
    rec_bytes = sum(3 * n for n in nsamp)
    need = start + rec_bytes * n_rec
    if len(raw) < need:
        raise ValueError("uncompiled BDF recording is absence")
    eeg_i = next((i for i, lab in enumerate(labels) if lab != "BDF Annotations"), None)
    if eeg_i is None:
        raise ValueError("uncompiled BDF recording is absence")
    tal_i = next((i for i, lab in enumerate(labels) if lab == "BDF Annotations"), None)
    off_eeg = sum(3 * nsamp[k] for k in range(eeg_i))
    samples = []
    tal_digital = []
    for rec in range(n_rec):
        base = start + rec * rec_bytes
        for j in range(nsamp[eeg_i]):
            samples.append(_from_i24(raw, base + off_eeg + 3 * j))
        if tal_i is not None:
            off_tal = sum(3 * nsamp[k] for k in range(tal_i))
            for j in range(nsamp[tal_i]):
                tal_digital.append(_from_i24(raw, base + off_tal + 3 * j))
    tal_raw = b"".join(_i24(int(x)) for x in tal_digital) if tal_i is not None else b""
    annotations = []
    if tal_raw:
        for ev in _TAL_RE.findall(tal_raw):
            onset = float(ev[0])
            duration = float(ev[2]) if ev[2] else 0.0
            for desc in ev[3].split(b"\x14")[1:]:
                text = desc.decode("ascii")
                if text:
                    annotations.append((onset, duration, text))
    return {
        "n_signals": 1,
        "n_samples": len(samples),
        "label": labels[eeg_i],
        "samples": samples,
        "annotations": annotations,
    }


def read_bdf_annotations(path):
    rec = read_bdf(path)
    texts = [row[2] for row in rec["annotations"]]
    if not texts:
        raise ValueError("uncompiled BDF recording is absence")
    return texts


def edf_occupancy(path):
    rec = read_edf(path)
    return rec["n_samples"]


def bdf_occupancy(path):
    rec = read_bdf(path)
    return rec["n_samples"]
