#!/usr/bin/env python3.12
"""Remainlock — two-modulus CRT check."""

from __future__ import annotations

import argparse
import sys

from crt import crt_pair


def verify_precision() -> str:
    if crt_pair(2, 3, 3, 5) != 8:
        raise SystemExit("crt identity failed")
    if crt_pair(2, 3, 3, 5) != crt_pair(2, 3, 3, 5):
        raise SystemExit("crt mismatch")
    try:
        crt_pair(2, 0, 3, 5)
    except ValueError:
        pass
    else:
        raise SystemExit("non-positive modulus accepted")
    try:
        crt_pair(2, 4, 3, 6)
    except ValueError:
        pass
    else:
        raise SystemExit("non-coprime moduli accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Remainlock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
