#!/usr/bin/env python3.12
"""Bloomlock — bloom maybe-membership check."""

from __future__ import annotations

import argparse
import sys

from bloom import bloom_maybe


def verify_precision() -> str:
    if bloom_maybe([1, 2, 3], 16, 2, 2) != 1:
        raise SystemExit("bloom identity failed")
    if bloom_maybe([1, 2, 3], 16, 2, 2) != bloom_maybe([1, 2, 3], 16, 2, 2):
        raise SystemExit("bloom mismatch")
    try:
        bloom_maybe([], 16, 2, 2)
    except ValueError:
        pass
    else:
        raise SystemExit("empty bloom accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Bloomlock — bloom maybe-membership check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
