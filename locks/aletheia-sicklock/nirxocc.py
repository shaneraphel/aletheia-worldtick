"""NIRx occupancy. An empty recording is absence, not 0 samples.

A NIRx folder is NIRStar 15.3 `hdr`/`inf`/`wl1`/`wl2`/`probeInfo.mat` plus
an `evt` of binary stim bits. Official MNE `read_raw_nirx` copies those
stims as annotation descriptions. An empty sample list or empty event list
refuses. NIRx stims are numeric, like Neuroscan CNT; Persyst and EyeLink
keep `trial_type` text.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import savemat

Z = -1


def _norm_events(events):
    if events is not None and not events:
        raise ValueError("uncompiled NIRx recording is absence")
    if events is None:
        events = [(1.0, 1), (2.0, 2)]
    rows = []
    for i, item in enumerate(events):
        if isinstance(item, int):
            onset, code = float(i + 1), int(item)
        elif len(item) >= 2:
            onset, code = float(item[0]), int(item[1])
        else:
            raise ValueError("uncompiled NIRx recording is absence")
        if code < 1:
            raise ValueError("uncompiled NIRx recording is absence")
        rows.append((int(onset), code))
    if not rows:
        raise ValueError("uncompiled NIRx recording is absence")
    return rows


def _evt_line(frame: int, code: int) -> str:
    bits = bin(code)[2:][::-1]
    return str(frame) + "".join(f" {b}" for b in bits)


def write_nirx(folder, samples, events=None):
    if samples is None or not samples:
        raise ValueError("uncompiled NIRx recording is absence")
    if events is not None and not events:
        raise ValueError("uncompiled NIRx recording is absence")
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    rows = _norm_events(events)
    (folder / "tape.hdr").write_text(
        "\n".join(
            [
                "[GeneralInfo]",
                'NIRStar="15.3"',
                'Device="NIRScout"',
                'Date="Mon, Sep 20, 2026"',
                'Time="14:00:00.000000"',
                "[ImagingParameters]",
                "Wavelengths=760 850",
                "SamplingRate=1",
                "[DataStructure]",
                "S-D-Key=1-1:1",
                "",
            ]
        )
    )
    (folder / "tape.inf").write_text(
        "\n".join(
            [
                "[Subject Demographics]",
                "name=aletheia tape",
                "gender=U",
                "age=26",
                "",
            ]
        )
    )
    (folder / "tape.set").write_text("set\n")
    (folder / "tape.tpl").write_text("tpl\n")
    (folder / "tape.config.txt").write_text("config\n")
    (folder / "tape.dat").write_bytes(b"\x00")
    (folder / "tape.wl1").write_text("\n".join(str(float(int(x))) for x in samples) + "\n")
    (folder / "tape.wl2").write_text("\n".join(str(float(int(x)) / 2) for x in samples) + "\n")
    (folder / "tape.evt").write_text("".join(_evt_line(f, c) + "\n" for f, c in rows))
    savemat(
        str(folder / "tape.probeInfo.mat"),
        {
            "probeInfo": {
                "probes": {
                    "index_c": np.array([[1, 1]], dtype=np.float64),
                    "coords_s3": np.array([[0.0, 0.0, 0.0]]),
                    "coords_d3": np.array([[10.0, 0.0, 0.0]]),
                    "coords_c3": np.array([[5.0, 0.0, 0.0]]),
                }
            }
        },
    )
    return folder


def read_nirx(folder):
    folder = Path(folder)
    wl1 = folder / "tape.wl1"
    if not wl1.exists():
        raise ValueError("uncompiled NIRx recording is absence")
    samples = [int(float(line)) for line in wl1.read_text().splitlines() if line.strip()]
    if not samples:
        raise ValueError("uncompiled NIRx recording is absence")
    return {"n_samples": len(samples), "samples": samples}


def read_nirx_evt(folder):
    evt = Path(folder) / "tape.evt"
    if not evt.exists():
        raise ValueError("uncompiled NIRx recording is absence")
    texts = []
    for line in evt.read_text().splitlines():
        toks = [t for t in line.split() if t]
        if len(toks) < 2:
            continue
        bits = "".join(toks[1:])[::-1]
        texts.append(f"{float(int(bits, 2))}")
    if not texts:
        raise ValueError("uncompiled NIRx recording is absence")
    return texts


def nirx_occupancy(folder):
    return read_nirx(folder)["n_samples"]
