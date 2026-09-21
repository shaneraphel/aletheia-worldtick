"""Curry occupancy. An empty recording is absence, not 0 samples.

A Curry 7 set is `.dap` / `.dat` / `.rs3` plus a `.cef` NUMBER_LIST.
Official MNE `read_raw_curry` copies those event codes as annotation
descriptions. An empty sample list or empty event list refuses. Curry
events are integer codes like Neuroscan CNT; Persyst and EyeLink keep
`trial_type` text.
"""
from __future__ import annotations

from pathlib import Path

Z = -1


def _norm_events(events):
    if events is not None and not events:
        raise ValueError("uncompiled Curry recording is absence")
    if events is None:
        events = [(1.0, 1), (2.0, 2)]
    rows = []
    for i, item in enumerate(events):
        if isinstance(item, int):
            onset, code = float(i + 1), int(item)
        elif len(item) >= 2:
            onset, code = float(item[0]), int(item[1])
        else:
            raise ValueError("uncompiled Curry recording is absence")
        if code < 1:
            raise ValueError("uncompiled Curry recording is absence")
        rows.append((int(onset), code))
    if not rows:
        raise ValueError("uncompiled Curry recording is absence")
    return rows


def _stem(path):
    path = Path(path)
    name = path.name
    base = name.split(".", maxsplit=1)[0]
    return path.with_name(base)


def write_curry(path, samples, events=None):
    if samples is None or not samples:
        raise ValueError("uncompiled Curry recording is absence")
    if events is not None and not events:
        raise ValueError("uncompiled Curry recording is absence")
    stem = _stem(path)
    stem.parent.mkdir(parents=True, exist_ok=True)
    rows = _norm_events(events)
    n = len(samples)
    stem.with_suffix(".dap").write_text(
        "\n".join(
            [
                f"NumSamples = {n}",
                "SampleFreqHz = 1",
                "DataFormat = ASCII",
                "SampleTimeUsec = 1000000",
                "NumChannels = 1",
                "StartYear = 2026",
                "StartMonth = 9",
                "StartDay = 21",
                "StartHour = 1",
                "StartMin = 0",
                "StartSec = 0",
                "StartMillisec = 0",
                "DEVICE_PARAMETERS START",
                "DATA_UNITS = uV",
                "",
            ]
        )
    )
    stem.with_suffix(".rs3").write_text(
        "\n".join(
            [
                "LABELS START_LIST",
                "Cz",
                "LABELS END_LIST",
                "SENSORS START_LIST",
                "0\t0\t80",
                "SENSORS END_LIST",
                "NORMALS START_LIST",
                "0\t0\t1",
                "NORMALS END_LIST",
                "",
            ]
        )
    )
    stem.with_suffix(".dat").write_text("\n".join(str(float(int(x))) for x in samples) + "\n")
    stem.with_suffix(".cef").write_text(
        "\n".join(
            ["NUMBER_LIST START_LIST"]
            + [f"{onset}\t0\t{code}" for onset, code in rows]
            + ["NUMBER_LIST END_LIST", ""]
        )
    )
    return stem.with_suffix(".dap")


def read_curry(path):
    dat = _stem(path).with_suffix(".dat")
    if not dat.exists() or dat.stat().st_size == 0:
        raise ValueError("uncompiled Curry recording is absence")
    samples = [int(float(line)) for line in dat.read_text().splitlines() if line.strip()]
    if not samples:
        raise ValueError("uncompiled Curry recording is absence")
    return {"n_samples": len(samples), "samples": samples}


def read_curry_cef(path):
    cef = _stem(path).with_suffix(".cef")
    if not cef.exists():
        raise ValueError("uncompiled Curry recording is absence")
    texts = []
    inside = False
    for line in cef.read_text().splitlines():
        if line.startswith("NUMBER_LIST END_LIST"):
            inside = False
        elif inside and line.strip():
            cols = line.split()
            if len(cols) >= 3:
                texts.append(str(int(cols[2])))
        elif line.startswith("NUMBER_LIST START_LIST"):
            inside = True
    if not texts:
        raise ValueError("uncompiled Curry recording is absence")
    return texts


def curry_occupancy(path):
    return read_curry(path)["n_samples"]
