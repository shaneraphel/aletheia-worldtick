#!/usr/bin/env python3.12
"""Cyclelock — Floyd cycle occupancy check."""

from __future__ import annotations

import argparse
import sys

from floyd import floyd_cycle


def verify_precision() -> str:
    if floyd_cycle([1, 2, 0]) != 1:
        raise SystemExit("floyd identity failed")
    if floyd_cycle([1, 2, 0]) != floyd_cycle([1, 2, 0]):
        raise SystemExit("floyd mismatch")
    try:
        floyd_cycle([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty floyd accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Cyclelock — Floyd cycle occupancy check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
