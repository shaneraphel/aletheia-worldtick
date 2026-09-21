"""SNIRF occupancy. An empty recording is absence, not 0 samples.

A SNIRF file is HDF5 `nirs/data1` plus optional `stim` tables. Official
MNE `read_raw_snirf` copies stim names as annotation descriptions. An
empty sample list or empty event list refuses. SNIRF stims are named
like NIRx numeric descriptions; Persyst and EyeLink keep `trial_type` text.
"""
from __future__ import annotations

from pathlib import Path

import h5py
import numpy as np

Z = -1


def _norm_events(events):
    if events is not None and not events:
        raise ValueError("uncompiled SNIRF recording is absence")
    if events is None:
        events = [(1.0, "1.0"), (2.0, "2.0")]
    rows = []
    for i, item in enumerate(events):
        if isinstance(item, str):
            onset, name = float(i + 1), item
        elif len(item) >= 2:
            onset, name = float(item[0]), str(item[1])
        else:
            raise ValueError("uncompiled SNIRF recording is absence")
        if not name:
            raise ValueError("uncompiled SNIRF recording is absence")
        rows.append((onset, name))
    if not rows:
        raise ValueError("uncompiled SNIRF recording is absence")
    return rows


def _s(text: str):
    return np.array(text, dtype="S")


def write_snirf(path, samples, events=None):
    if samples is None or not samples:
        raise ValueError("uncompiled SNIRF recording is absence")
    if events is not None and not events:
        raise ValueError("uncompiled SNIRF recording is absence")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = _norm_events(events)
    arr = np.array([int(x) for x in samples], dtype=np.float64)
    ts = np.column_stack([arr, arr / 2])
    t = np.arange(len(arr), dtype=np.float64)
    with h5py.File(path, "w") as f:
        nirs = f.create_group("nirs")
        data1 = nirs.create_group("data1")
        data1.create_dataset("dataTimeSeries", data=ts)
        data1.create_dataset("time", data=t)
        for i, widx in enumerate((1, 2), start=1):
            ml = data1.create_group(f"measurementList{i}")
            ml.create_dataset("dataType", data=1)
            ml.create_dataset("sourceIndex", data=1)
            ml.create_dataset("detectorIndex", data=1)
            ml.create_dataset("wavelengthIndex", data=widx)
            ml.create_dataset("dataTypeIndex", data=1)
        probe = nirs.create_group("probe")
        probe.create_dataset("wavelengths", data=np.array([760.0, 850.0]))
        probe.create_dataset("sourcePos3D", data=np.array([[0.0, 0.0, 0.0]]))
        probe.create_dataset("detectorPos3D", data=np.array([[0.03, 0.0, 0.0]]))
        md = nirs.create_group("metaDataTags")
        md.create_dataset("SubjectID", data=_s("aletheia"))
        md.create_dataset("MeasurementDate", data=_s("2026-09-20"))
        md.create_dataset("MeasurementTime", data=_s("14:00:00Z"))
        md.create_dataset("LengthUnit", data=_s("m"))
        md.create_dataset("TimeUnit", data=_s("s"))
        md.create_dataset("ManufacturerName", data=_s("aletheia"))
        for i, (onset, name) in enumerate(rows, start=1):
            stim = nirs.create_group(f"stim{i}")
            stim.create_dataset("name", data=_s(name))
            stim.create_dataset("data", data=np.array([[onset, 0.0, 1.0]]))
    return path


def read_snirf(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        raise ValueError("uncompiled SNIRF recording is absence")
    try:
        with h5py.File(path, "r") as f:
            if "nirs" not in f:
                raise ValueError("uncompiled SNIRF recording is absence")
            ts = np.array(f["nirs/data1/dataTimeSeries"])
    except (OSError, KeyError):
        raise ValueError("uncompiled SNIRF recording is absence") from None
    if ts.size == 0:
        raise ValueError("uncompiled SNIRF recording is absence")
    samples = [int(x) for x in ts[:, 0]]
    if not samples:
        raise ValueError("uncompiled SNIRF recording is absence")
    return {"n_samples": len(samples), "samples": samples}


def read_snirf_stim(path):
    path = Path(path)
    names = []
    with h5py.File(path, "r") as f:
        if "nirs" not in f:
            raise ValueError("uncompiled SNIRF recording is absence")
        for key in f["nirs"]:
            if "stim" not in key:
                continue
            raw = np.array(f[f"nirs/{key}/name"])
            if raw.shape == ():
                raw = raw[np.newaxis]
            names.append(raw[0].decode("UTF-8"))
    if not names:
        raise ValueError("uncompiled SNIRF recording is absence")
    return names


def snirf_occupancy(path):
    return read_snirf(path)["n_samples"]
