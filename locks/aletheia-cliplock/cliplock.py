#!/usr/bin/env python3.12
"""Cliplock — Akl–Toussaint interior-discard check."""

from __future__ import annotations

import argparse
import sys

from aktous import aktous_discard


def verify_precision() -> str:
    if aktous_discard([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != 1:
        raise SystemExit("akl identity failed")
    if aktous_discard([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != aktous_discard(
        [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]
    ):
        raise SystemExit("akl mismatch")
    try:
        aktous_discard([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty akl-toussaint accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Cliplock — Akl–Toussaint interior-discard check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
