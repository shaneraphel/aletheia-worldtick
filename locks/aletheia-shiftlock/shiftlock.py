#!/usr/bin/env python3.12
"""Shiftlock — job-schedule occupancy check."""
from __future__ import annotations
import argparse, sys
from jobsc import job_scheduling
def verify_precision() -> str:
    if job_scheduling([1,2,3,3],[3,4,5,6],[50,10,40,70])!=120:
        raise SystemExit("shift identity failed")
    if job_scheduling([1,2,3,3],[3,4,5,6],[50,10,40,70])!=job_scheduling([1,2,3,3],[3,4,5,6],[50,10,40,70]):
        raise SystemExit("shift mismatch")
    try: job_scheduling([],[],[])
    except ValueError: pass
    else: raise SystemExit("empty jobs accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Shiftlock — job-schedule occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
