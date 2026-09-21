#!/usr/bin/env python3.12
"""Twistlock — Givens and Householder occupancy check."""

from __future__ import annotations

import argparse
import sys

from givens import givens_hypot
from householder import householder_first


def verify_precision() -> str:
    if givens_hypot([3, 4]) != 5:
        raise SystemExit("givens identity failed")
    if givens_hypot([3, 4]) != givens_hypot([3, 4]):
        raise SystemExit("givens mismatch")
    if householder_first([3, 4, 12]) != -13:
        raise SystemExit("householder identity failed")
    if householder_first([3, 4, 12]) != householder_first([3, 4, 12]):
        raise SystemExit("householder mismatch")
    try:
        givens_hypot([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty givens accepted")
    try:
        householder_first([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty householder accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Twistlock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
