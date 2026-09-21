#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from pathlib import Path
from edfocc import edf_occupancy
from bidseeg import bids_eeg_occupancy
from xdfocc import xdf_occupancy
from bvocc import brainvision_occupancy
from wfdbocc import wfdb_occupancy

SEED, N_TRIALS, WARMUP = 20260919, 7, 1
ROOT = Path(__file__).resolve().parent / "resources" / "synthetic"
EDF = ROOT / "sub-01_task-spike_eeg.edf"
CH = ROOT / "sub-01_task-spike_channels.tsv"
EV = ROOT / "sub-01_task-spike_events.tsv"
XDF = ROOT / "sub-01_task-spike.xdf"
VHDR = ROOT / "sub-01_task-spike.vhdr"
HEA = ROOT / "sub-01_task-spike.hea"


def main():
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = edf_occupancy(EDF)
        at = time.perf_counter() - t0
        t1 = time.perf_counter()
        nv = edf_occupancy(EDF)
        bt = time.perf_counter() - t1
        if acc != nv:
            raise SystemExit("edf disagree")
        if trial < WARMUP:
            continue
        a.append(at)
        b.append(bt)
        first = acc if first is None else first
        second = acc
    if edf_occupancy(EDF) != 8:
        raise SystemExit("edf identity")
    if bids_eeg_occupancy(CH, EV) != 2:
        raise SystemExit("bids identity")
    if xdf_occupancy(XDF) != 1:
        raise SystemExit("xdf identity")
    if brainvision_occupancy(VHDR) != 8:
        raise SystemExit("brainvision identity")
    if wfdb_occupancy(HEA) != 8:
        raise SystemExit("wfdb identity")
    rec = {
        "schema": "spikelock.edfocc_bench.v1",
        "seed": SEED,
        "n_samples": 8,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(a),
        "edf_seconds_median": statistics.median(a),
        "repeat_seconds_median": statistics.median(b),
        "edf_seconds": a,
        "repeat_seconds": b,
        "samples_first": first,
        "samples_second": second,
        "samples_identical": first == second,
        "bids_occupancy": 2,
        "xdf_occupancy": 1,
        "brainvision_occupancy": 8,
        "wfdb_occupancy": 8,
        "edf_bytes": EDF.stat().st_size,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
