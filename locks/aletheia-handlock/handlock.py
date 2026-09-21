#!/usr/bin/env python3.12
"""Handlock — Hungarian assignment check."""

from __future__ import annotations

import argparse
import sys

from hungar import hungar_cost


def verify_precision() -> str:
    if hungar_cost([[1, 2], [2, 1]]) != 2:
        raise SystemExit("hungar identity failed")
    if hungar_cost([[1, 2], [2, 1]]) != hungar_cost([[1, 2], [2, 1]]):
        raise SystemExit("hungar mismatch")
    try:
        hungar_cost([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty cost accepted")
    try:
        hungar_cost([[1, 2]])
    except ValueError:
        pass
    else:
        raise SystemExit("non-square cost accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Handlock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
