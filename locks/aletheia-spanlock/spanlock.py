#!/usr/bin/env python3.12
"""Spanlock — segment-tree range-sum check."""

from __future__ import annotations

import argparse
import sys

from segspt import segspt_sum


def verify_precision() -> str:
    if segspt_sum([1, 3, 5, 7, 9], 1, 3) != 15:
        raise SystemExit("segspt identity failed")
    if segspt_sum([1, 3, 5, 7, 9], 1, 3) != segspt_sum([1, 3, 5, 7, 9], 1, 3):
        raise SystemExit("segspt mismatch")
    try:
        segspt_sum([], 0, 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty segspt accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Spanlock — segment-tree range-sum check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
