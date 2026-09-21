#!/usr/bin/env python3.12
"""Philock — SSA-phi check."""

from __future__ import annotations

import argparse
import sys

from ssa import ssa_phi_count


def verify_precision() -> str:
    if ssa_phi_count(3, [[], [], [0, 1]]) != 1:
        raise SystemExit("ssa identity failed")
    if ssa_phi_count(3, [[], [], [0, 1]]) != ssa_phi_count(3, [[], [], [0, 1]]):
        raise SystemExit("ssa mismatch")
    try:
        ssa_phi_count(0, [])
    except ValueError:
        pass
    else:
        raise SystemExit("empty cfg accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Philock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
