#!/usr/bin/env python3.12
"""Cuckoolock — cuckoo-hash occupancy check."""

from __future__ import annotations

import argparse
import sys

from cuckoo import cuckoo_placed


def verify_precision() -> str:
    if cuckoo_placed([3, 8, 12], 5) != 3:
        raise SystemExit("cuckoo identity failed")
    if cuckoo_placed([3, 8, 12], 5) != cuckoo_placed([3, 8, 12], 5):
        raise SystemExit("cuckoo mismatch")
    try:
        cuckoo_placed([], 5)
    except ValueError:
        pass
    else:
        raise SystemExit("empty cuckoo accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Cuckoolock — cuckoo-hash occupancy check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
