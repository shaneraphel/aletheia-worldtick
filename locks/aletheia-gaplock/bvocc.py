"""BrainVision occupancy. An empty recording is absence, not 0 channels.

OpenNeuro stores many EEG tapes as .vhdr / .vmrk / .eeg. This writer emits
Brain Vision Data Exchange 1.0, INT_16, one channel. Stimulus markers copy
BIDS trial_type into official MNE annotations. Zero channels or an empty
marker list refuse.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1


def write_brainvision(stem, samples, *, label="Cz", annotations=None):
    if samples is None or not samples:
        raise ValueError("uncompiled BrainVision recording is absence")
    if annotations is not None and not annotations:
        raise ValueError("uncompiled BrainVision recording is absence")
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    eeg = stem.with_suffix(".eeg")
    vhdr = stem.with_suffix(".vhdr")
    vmrk = stem.with_suffix(".vmrk")
    eeg.write_bytes(b"".join(struct.pack("<h", int(x)) for x in samples))
    interval = "1000000" if annotations is not None else "125000"
    vhdr.write_text(
        "Brain Vision Data Exchange Header File Version 1.0\n"
        "[Common Infos]\n"
        f"DataFile={eeg.name}\n"
        f"MarkerFile={vmrk.name}\n"
        "DataFormat=BINARY\n"
        "DataOrientation=MULTIPLEXED\n"
        "NumberOfChannels=1\n"
        f"SamplingInterval={interval}\n"
        "[Binary Infos]\n"
        "BinaryFormat=INT_16\n"
        "[Channel Infos]\n"
        f"Ch1={label},,1,uV\n"
    )
    marks = ["Mk1=New Segment,,1,1,0\n"]
    if annotations is not None:
        sfreq = 1_000_000.0 / float(interval)
        for i, item in enumerate(annotations):
            if item is None:
                raise ValueError("uncompiled BrainVision recording is absence")
            if isinstance(item, str):
                onset, text = float(i + 1), item
            elif len(item) >= 2:
                onset, text = float(item[0]), str(item[1])
            else:
                raise ValueError("uncompiled BrainVision recording is absence")
            if not text or not text.isascii() or "," in text:
                raise ValueError("uncompiled BrainVision recording is absence")
            pos = int(round(onset * sfreq)) + 1
            if pos < 1:
                raise ValueError("uncompiled BrainVision recording is absence")
            marks.append(f"Mk{i + 2}=Stimulus,{text},{pos},1,0\n")
    vmrk.write_text(
        "Brain Vision Data Exchange Marker File, Version 1.0\n"
        "[Common Infos]\n"
        f"DataFile={eeg.name}\n"
        "[Marker Infos]\n" + "".join(marks)
    )
    return vhdr


def read_brainvision(vhdr):
    p = Path(vhdr)
    if not p.exists():
        raise ValueError("uncompiled BrainVision recording is absence")
    text = p.read_text()
    if "NumberOfChannels=0" in text or "NumberOfChannels=" not in text:
        raise ValueError("uncompiled BrainVision recording is absence")
    n = None
    data_name = None
    for ln in text.splitlines():
        if ln.startswith("NumberOfChannels="):
            n = int(ln.split("=", 1)[1])
        if ln.startswith("DataFile="):
            data_name = ln.split("=", 1)[1].strip()
    if n is None or n < 1 or not data_name:
        raise ValueError("uncompiled BrainVision recording is absence")
    raw = (p.parent / data_name).read_bytes()
    if len(raw) < 2:
        raise ValueError("uncompiled BrainVision recording is absence")
    samples = [struct.unpack_from("<h", raw, 2 * i)[0] for i in range(len(raw) // 2)]
    return {"n_channels": n, "n_samples": len(samples), "samples": samples}


def read_brainvision_annotations(path):
    p = Path(path)
    if p.suffix == ".vhdr":
        if not p.exists():
            raise ValueError("uncompiled BrainVision recording is absence")
        marker_name = None
        for ln in p.read_text().splitlines():
            if ln.startswith("MarkerFile="):
                marker_name = ln.split("=", 1)[1].strip()
        if not marker_name:
            raise ValueError("uncompiled BrainVision recording is absence")
        p = p.parent / marker_name
    if not p.exists():
        raise ValueError("uncompiled BrainVision recording is absence")
    texts = []
    for ln in p.read_text().splitlines():
        if not ln.startswith("Mk") or "=" not in ln:
            continue
        parts = ln.split("=", 1)[1].split(",")
        if len(parts) < 4:
            continue
        mtype, mdesc = parts[0], parts[1]
        if mtype == "New Segment" or not mdesc:
            continue
        texts.append(mdesc)
    if not texts:
        raise ValueError("uncompiled BrainVision recording is absence")
    return texts


def brainvision_occupancy(vhdr):
    return read_brainvision(vhdr)["n_samples"]
