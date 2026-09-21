#!/usr/bin/env python3.12
"""Pairlock — blossom matching check."""

from __future__ import annotations

import argparse
import sys

from blossom import blossom_match


def verify_precision() -> str:
    if blossom_match(4, [(0, 1), (2, 3)]) != 2:
        raise SystemExit("blossom identity failed")
    if blossom_match(4, [(0, 1), (2, 3)]) != blossom_match(4, [(0, 1), (2, 3)]):
        raise SystemExit("blossom mismatch")
    if blossom_match(3, []) != 0:
        raise SystemExit("isolated matching failed")
    try:
        blossom_match(0, [])
    except ValueError:
        pass
    else:
        raise SystemExit("empty vertex set accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Pairlock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
