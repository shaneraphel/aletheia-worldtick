"""EEGLAB occupancy. An empty set is absence, not 0 points.

EEGLAB `.set` is a MATLAB v5 file with an EEG struct. Zero `pnts` refuse.
`EEG.event` is a list of structs with `type` and 1-based `latency`.
Official MNE onset is `(latency-1)/srate`. Empty events refuse.
This writer uses SciPy `savemat`. It is not a second BioSig GDF writer.
"""
from __future__ import annotations

from pathlib import Path

Z = -1


def _norm_events(events):
    if events is not None and not events:
        raise ValueError("uncompiled EEGLAB set is absence")
    if events is None:
        events = [{"type": "go", "latency": 2.0}, {"type": "end", "latency": 3.0}]
    rows = []
    for ev in events:
        if not isinstance(ev, dict):
            raise ValueError("uncompiled EEGLAB set is absence")
        typ = ev.get("type")
        if typ is None or str(typ) == "":
            raise ValueError("uncompiled EEGLAB set is absence")
        if "latency" not in ev:
            raise ValueError("uncompiled EEGLAB set is absence")
        row = {"type": str(typ), "latency": float(ev["latency"])}
        if "duration" in ev:
            row["duration"] = float(ev["duration"])
        if "channel" in ev:
            row["channel"] = int(ev["channel"])
        rows.append(row)
    keys = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    for row in rows:
        for key in keys:
            if key not in row:
                row[key] = 0.0 if key == "duration" else 0
    return rows


def write_eeglab(path, samples, events=None, n_chan=1):
    if samples is None or not samples:
        raise ValueError("uncompiled EEGLAB set is absence")
    if n_chan < 1:
        raise ValueError("uncompiled EEGLAB set is absence")
    from scipy.io import savemat
    import numpy as np

    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    col = np.asarray(list(samples), dtype=np.float64).reshape(-1)
    data = np.tile(col, (n_chan, 1))
    savemat(
        dest,
        {
            "EEG": {
                "setname": "aletheia",
                "nbchan": int(n_chan),
                "pnts": int(data.shape[1]),
                "srate": 1.0,
                "trials": 1,
                "data": data,
                "event": _norm_events(events),
            }
        },
    )
    return dest


def _eeg(path):
    dest = Path(path)
    if not dest.exists() or dest.stat().st_size < 16:
        raise ValueError("uncompiled EEGLAB set is absence")
    from scipy.io import loadmat

    rec = loadmat(dest, squeeze_me=True, struct_as_record=False)
    eeg = rec.get("EEG")
    if eeg is None:
        raise ValueError("uncompiled EEGLAB set is absence")
    return eeg


def read_eeglab(path):
    import numpy as np

    data = np.atleast_1d(np.asarray(_eeg(path).data, dtype=np.float64)).reshape(-1)
    if data.size < 1:
        raise ValueError("uncompiled EEGLAB set is absence")
    return [int(v) for v in data.tolist()]


def read_eeglab_events(path):
    import numpy as np

    ev = getattr(_eeg(path), "event", None)
    if ev is None:
        raise ValueError("uncompiled EEGLAB set is absence")
    types = []
    for e in np.atleast_1d(ev):
        t = getattr(e, "type", "")
        if t is None or str(t) == "":
            continue
        types.append(str(t))
    if not types:
        raise ValueError("uncompiled EEGLAB set is absence")
    return types


def read_eeglab_word(path):
    word = "".join(read_eeglab_events(path))
    if not word:
        raise ValueError("uncompiled EEGLAB set is absence")
    return word


def read_eeglab_sick(path):
    import numpy as np

    eeg = _eeg(path)
    n = int(eeg.nbchan)
    if n < 1:
        raise ValueError("uncompiled EEGLAB set is absence")
    ev = getattr(eeg, "event", None)
    if ev is None:
        raise ValueError("uncompiled EEGLAB set is absence")
    sick = [int(getattr(e, "channel")) for e in np.atleast_1d(ev)]
    if not sick:
        raise ValueError("uncompiled EEGLAB set is absence")
    return n, sick


def eeglab_occupancy(path):
    return len(read_eeglab(path))
