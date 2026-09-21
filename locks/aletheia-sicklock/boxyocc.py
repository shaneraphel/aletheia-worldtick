"""BOXY occupancy. An empty recording is absence, not 0 samples.

An ISS Imagent BOXY 0.84 parsed file is tab-separated `A-DC1` plus `digaux`.
Official MNE `read_raw_boxy` copies those markers as annotation
descriptions. An empty sample list or empty event list refuses. BOXY
markers are numeric like NIRx and SNIRF; Persyst and EyeLink keep
`trial_type` text.
"""
from __future__ import annotations

from pathlib import Path

Z = -1


def _norm_events(events):
    if events is not None and not events:
        raise ValueError("uncompiled BOXY recording is absence")
    if events is None:
        events = [(1.0, 1), (2.0, 2)]
    rows = []
    for i, item in enumerate(events):
        if isinstance(item, int):
            onset, code = float(i + 1), int(item)
        elif len(item) >= 2:
            onset, code = float(item[0]), int(item[1])
        else:
            raise ValueError("uncompiled BOXY recording is absence")
        if code < 1:
            raise ValueError("uncompiled BOXY recording is absence")
        rows.append((int(onset), code))
    if not rows:
        raise ValueError("uncompiled BOXY recording is absence")
    return rows


def write_boxy(path, samples, events=None):
    if samples is None or not samples:
        raise ValueError("uncompiled BOXY recording is absence")
    if events is not None and not events:
        raise ValueError("uncompiled BOXY recording is absence")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    marks = {t: c for t, c in _norm_events(events)}
    lines = [
        "BOXY.EXE: ISS Imagent 0.84",
        "1 Detector Channels",
        "1 External MUX Channels",
        "1 Update Rate (Hz)",
        "",
        "#DATA BEGINS",
        "time,A-DC1,A-AC1,A-Ph1,digaux",
        "dummy",
    ]
    for t, s in enumerate(samples):
        lines.append("\t".join([str(t), str(float(int(s))), "0", "0", str(marks.get(t, 0))]))
    # MNE only closes a digaux run when the marker returns to 0.
    lines.append("\t".join([str(len(samples)), "0", "0", "0", "0"]))
    lines.append("#DATA ENDS")
    path.write_text("\n".join(lines) + "\n")
    return path


def read_boxy(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        raise ValueError("uncompiled BOXY recording is absence")
    text = path.read_text()
    if "#DATA BEGINS" not in text:
        raise ValueError("uncompiled BOXY recording is absence")
    body = text.split("#DATA BEGINS", 1)[1]
    if "#DATA ENDS" in body:
        body = body.split("#DATA ENDS", 1)[0]
    samples = []
    for ln in body.splitlines():
        if not ln.strip() or ln.startswith("time") or ln.startswith("dummy"):
            continue
        cols = ln.split()
        if len(cols) < 2:
            continue
        samples.append(int(float(cols[1])))
    if len(samples) < 2:
        raise ValueError("uncompiled BOXY recording is absence")
    samples = samples[:-1]  # drop the marker-closer row
    if not samples:
        raise ValueError("uncompiled BOXY recording is absence")
    return {"n_samples": len(samples), "samples": samples}


def read_boxy_digaux(path):
    path = Path(path)
    texts = []
    for ln in path.read_text().splitlines():
        if not ln.strip() or ln.startswith("time") or ln.startswith("dummy") or ln.startswith("#") or ln.startswith("BOXY") or "Channels" in ln or "Rate" in ln:
            continue
        cols = ln.split()
        if len(cols) < 5:
            continue
        code = int(float(cols[4]))
        if code >= 1:
            texts.append(f"{float(code)}")
    if not texts:
        raise ValueError("uncompiled BOXY recording is absence")
    return texts


def boxy_occupancy(path):
    return read_boxy(path)["n_samples"]
