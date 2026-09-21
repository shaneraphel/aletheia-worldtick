#!/usr/bin/env python3.12
"""Wavelock — prefix-rank check."""

from __future__ import annotations

import argparse
import sys

from wavelet import wavelet_rank


def verify_precision() -> str:
    if wavelet_rank([1, 2, 1, 3, 1], 1, 5) != 3:
        raise SystemExit("wavelet identity failed")
    if wavelet_rank([1, 2, 1, 3, 1], 1, 5) != wavelet_rank([1, 2, 1, 3, 1], 1, 5):
        raise SystemExit("wavelet mismatch")
    try:
        wavelet_rank([], 1, 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty sequence accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Wavelock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
