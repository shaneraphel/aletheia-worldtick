"""Persyst occupancy. An empty recording is absence, not 0 channels.

Persyst stores a `.lay` INI header beside a `.dat` of int16 samples.
`[Comments]` lines are `onset,duration,state,type,text`. Official MNE
`read_raw_persyst` copies that text into annotation descriptions. An empty
sample list or empty comment list refuses. ANT Neuro CNT stays Z until
`antio` is present.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1


def _norm_comments(comments):
    if comments is not None and not comments:
        raise ValueError("uncompiled Persyst recording is absence")
    if comments is None:
        comments = [(1.0, "go"), (2.0, "end")]
    rows = []
    for i, item in enumerate(comments):
        if isinstance(item, str):
            onset, text = float(i + 1), item
        elif isinstance(item, dict):
            onset, text = float(item["onset"]), str(item["text"])
        elif len(item) >= 2:
            onset, text = float(item[0]), str(item[1])
        else:
            raise ValueError("uncompiled Persyst recording is absence")
        if not text or not text.isascii() or "," in text:
            raise ValueError("uncompiled Persyst recording is absence")
        rows.append((float(onset), text))
    if not rows:
        raise ValueError("uncompiled Persyst recording is absence")
    return rows


def write_persyst(stem, samples, comments=None, *, label="Cz"):
    if samples is None or not samples:
        raise ValueError("uncompiled Persyst recording is absence")
    if comments is not None and not comments:
        raise ValueError("uncompiled Persyst recording is absence")
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    rec = stem.name
    lay = stem.with_suffix(".lay")
    dat = stem.with_suffix(".dat")
    n = len(samples)
    rows = _norm_comments(comments)
    dat.write_bytes(b"".join(struct.pack("<h", int(x)) for x in samples))
    comment_lines = "\n".join(f"{onset:.6f},0.000000,0,0,{text}" for onset, text in rows)
    lay.write_text(
        "\n".join(
            [
                "[FileInfo]",
                f"File={rec}.dat",
                "FileType=EEG",
                "Rate=1",
                "Datatype=0",
                "Calibration=1",
                "WaveformCount=1",
                "SamplingRate=1",
                "[ChannelMap]",
                f"{label}-Ref=1",
                "[Patient]",
                "TestDate=09/20/2026",
                "TestTime=14:00:00",
                "BirthDate=01/01/90",
                "First=aletheia",
                "Last=tape",
                "Sex=U",
                "Hand=U",
                "[Comments]",
                comment_lines,
                "",
            ]
        )
    )
    return lay


def _lay_dat(path):
    p = Path(path)
    if p.suffix == ".dat":
        return p.with_suffix(".lay"), p
    if p.suffix == ".lay":
        return p, p.with_suffix(".dat")
    return p.with_suffix(".lay"), p.with_suffix(".dat")


def read_persyst(path):
    lay, dat = _lay_dat(path)
    if not lay.exists() or not dat.exists():
        raise ValueError("uncompiled Persyst recording is absence")
    raw = dat.read_bytes()
    if len(raw) < 2:
        raise ValueError("uncompiled Persyst recording is absence")
    samples = [struct.unpack_from("<h", raw, 2 * i)[0] for i in range(len(raw) // 2)]
    if not samples:
        raise ValueError("uncompiled Persyst recording is absence")
    return {"n_samples": len(samples), "samples": samples}


def read_persyst_comments(path):
    lay, _dat = _lay_dat(path)
    if not lay.exists():
        raise ValueError("uncompiled Persyst recording is absence")
    section = ""
    texts = []
    for line in lay.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].lower()
            continue
        if section != "comments":
            continue
        parts = line.split(",", 4)
        if len(parts) < 5:
            raise ValueError("uncompiled Persyst recording is absence")
        text = parts[4]
        if not text:
            continue
        texts.append(text)
    if not texts:
        raise ValueError("uncompiled Persyst recording is absence")
    return texts


def persyst_occupancy(path):
    return read_persyst(path)["n_samples"]
