#!/usr/bin/env python3.12
"""Marchlock — Jarvis hull-occupancy check."""

from __future__ import annotations

import argparse
import sys

from jarvis import jarvis_hull


def verify_precision() -> str:
    if jarvis_hull([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != 4:
        raise SystemExit("jarvis identity failed")
    if jarvis_hull([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != jarvis_hull(
        [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]
    ):
        raise SystemExit("jarvis mismatch")
    try:
        jarvis_hull([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty jarvis accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Marchlock — Jarvis hull-occupancy check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
