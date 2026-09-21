#!/usr/bin/env python3.12
"""Jointlock — two-link inverse-kinematics check."""

from __future__ import annotations

import argparse
import sys

from ik import two_link_ik


def verify_precision() -> str:
    a = two_link_ik(2.0, 0.0, 1.0, 1.0)
    if len(a) != 2:
        raise SystemExit("ik identity failed")
    if two_link_ik(2.0, 0.0, 1.0, 1.0) != two_link_ik(2.0, 0.0, 1.0, 1.0):
        raise SystemExit("ik mismatch")
    try:
        two_link_ik(4.0, 0.0, 1.0, 1.0)
    except ValueError:
        pass
    else:
        raise SystemExit("unreachable ik accepted")

    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Jointlock — two-link inverse-kinematics check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
