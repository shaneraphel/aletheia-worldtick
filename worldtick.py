#!/usr/bin/env python3.12
"""Worldtick — fact-reachability check."""

from __future__ import annotations

import argparse
import sys

from datalog import datalog_fixpoint


def verify_precision() -> str:
    if datalog_fixpoint(3, [0], [(0, 1), (1, 2)]) != 3:
        raise SystemExit("datalog identity failed")
    if datalog_fixpoint(3, [0], [(0, 1), (1, 2)]) != datalog_fixpoint(3, [0], [(0, 1), (1, 2)]):
        raise SystemExit("datalog mismatch")
    try:
        datalog_fixpoint(3, [], [(0, 1)])
    except ValueError:
        pass
    else:
        raise SystemExit("empty facts accepted")
    try:
        datalog_fixpoint(-1, [0], [(0, 1)])
    except ValueError:
        pass
    else:
        raise SystemExit("negative n accepted")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Worldtick precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
