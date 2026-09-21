#!/usr/bin/env python3.12
"""Prefixlock — Fenwick prefix-sum check."""

from __future__ import annotations

import argparse
import sys

from fenwick import fenwick_prefix


def verify_precision() -> str:
    if fenwick_prefix([1, 2, 3, 4], 3) != 10:
        raise SystemExit("fenwick identity failed")
    if fenwick_prefix([1, 2, 3, 4], 3) != fenwick_prefix([1, 2, 3, 4], 3):
        raise SystemExit("fenwick mismatch")
    try:
        fenwick_prefix([], 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty fenwick accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Prefixlock — Fenwick prefix-sum check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
