"""BIDS-EEG occupancy. An empty channels or events table is absence, not 0 rows.

trial_type copies into an official MNE annotations .txt as description.
An empty trial_type list or empty annotations file refuses. Official MNE
reads an empty .txt as 0 descriptions.
"""
from __future__ import annotations

from pathlib import Path

Z = -1


def _rows(path):
    p = Path(path)
    if not p.exists():
        raise ValueError("uncompiled BIDS-EEG table is absence")
    lines = [ln for ln in p.read_text().splitlines() if ln.strip()]
    if len(lines) < 2:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    header = lines[0].split("\t")
    body = [ln.split("\t") for ln in lines[1:]]
    if not header or not body:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    return header, body


def write_bids_eeg(channels_tsv, events_tsv, names, onsets, trial_types=None):
    if not names or not onsets:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    types = [str(t) for t in (trial_types if trial_types is not None else ["event"] * len(onsets))]
    if len(types) != len(onsets) or any(not t for t in types):
        raise ValueError("uncompiled BIDS-EEG table is absence")
    ch = Path(channels_tsv)
    ev = Path(events_tsv)
    ch.parent.mkdir(parents=True, exist_ok=True)
    ev.parent.mkdir(parents=True, exist_ok=True)
    ch.write_text("name\ttype\tunits\n" + "".join(f"{n}\tEEG\tuV\n" for n in names))
    ev.write_text(
        "onset\tduration\ttrial_type\n"
        + "".join(f"{int(o)}\t0\t{t}\n" for o, t in zip(onsets, types))
    )
    return ch, ev


def write_bids_marker_events(events_tsv, markers, onsets=None):
    labs = [str(m) for m in markers]
    if not labs or any(not t for t in labs):
        raise ValueError("uncompiled BIDS-EEG table is absence")
    ons = list(onsets) if onsets is not None else list(range(1, len(labs) + 1))
    if len(ons) != len(labs):
        raise ValueError("uncompiled BIDS-EEG table is absence")
    ev = Path(events_tsv)
    ev.parent.mkdir(parents=True, exist_ok=True)
    ev.write_text(
        "onset\tduration\ttrial_type\n"
        + "".join(f"{int(o)}\t0\t{t}\n" for o, t in zip(ons, labs))
    )
    return ev


def read_bids_onsets(events_tsv):
    ev_h, ev = _rows(events_tsv)
    if "onset" not in ev_h:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    i = ev_h.index("onset")
    onsets = [int(float(row[i])) for row in ev]
    if not onsets:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    return onsets


def read_bids_trial_types(events_tsv):
    ev_h, ev = _rows(events_tsv)
    if "trial_type" not in ev_h:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    i = ev_h.index("trial_type")
    types = [row[i] for row in ev]
    if not types or any(not t for t in types):
        raise ValueError("uncompiled BIDS-EEG table is absence")
    return types


def read_bids_durations(events_tsv):
    ev_h, ev = _rows(events_tsv)
    if "duration" not in ev_h:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    i = ev_h.index("duration")
    durs = [float(row[i]) for row in ev]
    if not durs:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    return durs


def _annot_num(x):
    v = float(x)
    if v.is_integer():
        return f"{v:.1f}"
    return str(v)


def write_mne_annot(path, onsets, descriptions, durations=None):
    labs = [str(d) for d in descriptions]
    if not labs or any(not t or not t.isascii() or "," in t for t in labs):
        raise ValueError("uncompiled BIDS-EEG table is absence")
    ons = [float(o) for o in onsets]
    if not ons or len(ons) != len(labs):
        raise ValueError("uncompiled BIDS-EEG table is absence")
    durs = [float(d) for d in (durations if durations is not None else [0.0] * len(ons))]
    if len(durs) != len(labs):
        raise ValueError("uncompiled BIDS-EEG table is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    body = "# MNE-Annotations\n# onset, duration, description\n"
    body += "".join(f"{_annot_num(o)},{_annot_num(d)},{lab}\n" for o, d, lab in zip(ons, durs, labs))
    dest.write_text(body)
    return dest


def write_mne_annot_from_bids(events_tsv, annot_txt):
    return write_mne_annot(
        annot_txt,
        read_bids_onsets(events_tsv),
        read_bids_trial_types(events_tsv),
        read_bids_durations(events_tsv),
    )


def read_mne_annot(path):
    raw = Path(path).read_text() if Path(path).exists() else ""
    rows = []
    for ln in raw.splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        parts = ln.split(",")
        if len(parts) < 3:
            raise ValueError("uncompiled BIDS-EEG table is absence")
        desc = parts[2].strip()
        if not desc:
            raise ValueError("uncompiled BIDS-EEG table is absence")
        rows.append((float(parts[0]), float(parts[1]), desc))
    if not rows:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    return rows


def read_mne_annot_descriptions(path):
    return [row[2] for row in read_mne_annot(path)]


def bids_eeg_occupancy(channels_tsv, events_tsv):
    ch_h, ch = _rows(channels_tsv)
    ev_h, ev = _rows(events_tsv)
    if "name" not in ch_h or "onset" not in ev_h:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    return len(ch) + len(ev)
