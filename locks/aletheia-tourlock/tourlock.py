#!/usr/bin/env python3.12
"""Tourlock — visit-every-node occupancy check."""
from __future__ import annotations
import argparse, sys
from visitall import shortest_path_visit
G=[[1,2,3],[0],[0],[0]]
def verify_precision() -> str:
    if shortest_path_visit(G)!=4: raise SystemExit("tour identity failed")
    if shortest_path_visit(G)!=shortest_path_visit(G): raise SystemExit("tour mismatch")
    try: shortest_path_visit([])
    except ValueError: pass
    else: raise SystemExit("empty graph accepted")
    return "ok"
def main() -> int:
    p=argparse.ArgumentParser(description="Tourlock — visit-every-node occupancy check")
    p.add_argument("--verify-precision", action="store_true")
    args=p.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision()); return 0
    p.print_help(); return 2
if __name__=="__main__":
    raise SystemExit(main())
