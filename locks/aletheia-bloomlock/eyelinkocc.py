"""EyeLink occupancy. An empty recording is absence, not 0 samples.

SR Research EyeLink `.asc` is START/SAMPLES/PUPIL/MSG/END text. Official MNE
`read_raw_eyelink` copies MSG text into annotation descriptions. An empty
sample list or empty message list refuses. Gaze is a different modality from
EEG; Persyst and Nihon Kohden remain the clinical comment channels.
"""
from __future__ import annotations

from pathlib import Path

Z = -1


def _norm_msg(messages):
    if messages is not None and not messages:
        raise ValueError("uncompiled EyeLink recording is absence")
    if messages is None:
        messages = [(1.0, "go"), (2.0, "end")]
    rows = []
    for i, item in enumerate(messages):
        if isinstance(item, str):
            onset, text = float(i + 1), item
        elif len(item) >= 2:
            onset, text = float(item[0]), str(item[1])
        else:
            raise ValueError("uncompiled EyeLink recording is absence")
        if not text or not text.isascii() or " " in text:
            raise ValueError("uncompiled EyeLink recording is absence")
        rows.append((onset, text))
    if not rows:
        raise ValueError("uncompiled EyeLink recording is absence")
    return rows


def write_eyelink(path, samples, messages=None):
    if samples is None or not samples:
        raise ValueError("uncompiled EyeLink recording is absence")
    if messages is not None and not messages:
        raise ValueError("uncompiled EyeLink recording is absence")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = _norm_msg(messages)
    lines = [
        "START\t0\tLEFT\tSAMPLES\tEVENTS",
        "PUPIL\tAREA",
        "SAMPLES\tGAZE\tLEFT\tRATE\t1.00\tTRACKING\tCR\tFILTER\t2",
    ]
    for i, x in enumerate(samples):
        t = i * 1000
        lines.append(f"{t}\t512.0\t384.0\t{float(int(x))}")
    for onset, text in rows:
        lines.append(f"MSG\t{int(onset * 1000)} {text}")
    lines.append(f"END\t{(len(samples) - 1) * 1000}\tSAMPLES\tEVENTS")
    path.write_text("\n".join(lines) + "\n")
    return path


def read_eyelink(path):
    path = Path(path)
    samples = []
    for line in path.read_text().splitlines():
        toks = line.split()
        if not toks or not toks[0][0].isnumeric():
            continue
        if len(toks) < 4:
            raise ValueError("uncompiled EyeLink recording is absence")
        samples.append(int(float(toks[3])))
    if not samples:
        raise ValueError("uncompiled EyeLink recording is absence")
    return {"n_samples": len(samples), "samples": samples}


def read_eyelink_msg(path):
    path = Path(path)
    texts = []
    for line in path.read_text().splitlines():
        if not line.startswith("MSG"):
            continue
        parts = line.split(None, 2)
        if len(parts) < 3:
            continue
        text = parts[2]
        if text:
            texts.append(text)
    if not texts:
        raise ValueError("uncompiled EyeLink recording is absence")
    return texts


def eyelink_occupancy(path):
    return read_eyelink(path)["n_samples"]
