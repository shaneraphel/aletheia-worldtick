#!/usr/bin/env python3.12
"""Pulselock — k-subarray strength occupancy check."""
from __future__ import annotations
import argparse, sys
from kstren import max_k_subarray_strength
NUMS=[1,2,3,-1,2]
def verify_precision() -> str:
    if max_k_subarray_strength(NUMS, 3)!=22: raise SystemExit("pulse identity failed")
    if max_k_subarray_strength(NUMS, 3)!=max_k_subarray_strength(NUMS, 3): raise SystemExit("pulse mismatch")
    try: max_k_subarray_strength([], 1)
    except ValueError: pass
    else: raise SystemExit("empty nums accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Pulselock — k-subarray strength occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
