#!/usr/bin/env python3.12
"""Spikelock — sample-occupancy check."""

from __future__ import annotations

import argparse
import sys

from pathlib import Path

from bidseeg import bids_eeg_occupancy
from edfocc import edf_occupancy
from nyqst import nyquist
from xdfocc import xdf_occupancy

SYN = Path(__file__).resolve().parent / "resources" / "synthetic"


def verify_precision() -> str:
    if nyquist([(4, 0), (4, 1), (2, 0)]) != 3:
        raise SystemExit("nyquist identity failed")
    if nyquist([(4, 0), (4, 1), (2, 0)]) != nyquist([(4, 0), (4, 1), (2, 0)]):
        raise SystemExit("nyquist mismatch")
    try:
        nyquist([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty tape accepted")
    try:
        nyquist([(0, 0)])
    except ValueError:
        pass
    else:
        raise SystemExit("nonpositive sample count accepted")
    if edf_occupancy(SYN / "sub-01_task-spike_eeg.edf") != 8:
        raise SystemExit("edf identity failed")
    if bids_eeg_occupancy(SYN / "sub-01_task-spike_channels.tsv", SYN / "sub-01_task-spike_events.tsv") != 2:
        raise SystemExit("bids identity failed")
    if xdf_occupancy(SYN / "sub-01_task-spike.xdf") != 1:
        raise SystemExit("xdf identity failed")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Spikelock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
