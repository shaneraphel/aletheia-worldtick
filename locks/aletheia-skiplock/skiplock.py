#!/usr/bin/env python3.12
"""Skiplock — skip-search check."""

from __future__ import annotations

import argparse
import sys

from skiplist import skip_search


def verify_precision() -> str:
    if skip_search([1, 3, 5, 7], 5) != 2:
        raise SystemExit("skip identity failed")
    if skip_search([1, 3, 5, 7], 5) != skip_search([1, 3, 5, 7], 5):
        raise SystemExit("skip mismatch")
    try:
        skip_search([], 5)
    except ValueError:
        pass
    else:
        raise SystemExit("empty list accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Skiplock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
