#!/usr/bin/env python3.12
"""Reachlock — hashable two-link reach and integer disk clearance."""

from __future__ import annotations

import argparse
import hashlib
import sys

from reach import two_link_ik
from sdfocc import disk_clearance2, signed_distance_occupancy

DISKS: tuple[tuple[int, int, int], ...] = ((80, 40, 18), (20, 70, 14), (110, 90, 16))
FIELD_ORIGIN = (0, 0)
FIELD_SPAN = 160
FIELD_STEP = 8


def field_digest(
    disks: tuple[tuple[int, int, int], ...],
    origin: tuple[int, int] = FIELD_ORIGIN,
    span: int = FIELD_SPAN,
    step: int = FIELD_STEP,
) -> str:
    if not disks:
        raise ValueError("empty field is absence")
    acc: list[bytes] = []
    ox, oy = origin
    for y in range(oy, oy + span, step):
        for x in range(ox, ox + span, step):
            best: int | None = None
            for cx, cy, radius in disks:
                clearance = disk_clearance2(x, y, cx, cy, radius)
                best = clearance if best is None else min(best, clearance)
            acc.append(str(best).encode())
    return hashlib.sha256(b"\n".join(acc)).hexdigest()


def verify_precision() -> str:
    first = two_link_ik(2.0, 0.0, 1.0, 1.0)
    second = two_link_ik(2.0, 0.0, 1.0, 1.0)
    if first != second:
        raise SystemExit("reach mismatch")
    try:
        two_link_ik(3.0, 0.0, 1.0, 1.0)
    except ValueError:
        pass
    else:
        raise SystemExit("unreachable accepted")
    if disk_clearance2(3, 0, 0, 0, 3) != 0:
        raise SystemExit("surface clearance is not 0")
    digest_a = field_digest(DISKS)
    digest_b = field_digest(DISKS)
    if digest_a != digest_b:
        raise SystemExit("field digest mismatch")
    if signed_distance_occupancy([(3, 0), (4, 1), (2, 0)]) != 3:
        raise SystemExit("named-sample count mismatch")
    try:
        signed_distance_occupancy([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty field accepted")
    try:
        field_digest(())
    except ValueError:
        pass
    else:
        raise SystemExit("empty disks accepted")
    return digest_a


def main() -> int:
    parser = argparse.ArgumentParser(description="Reachlock precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        digest = verify_precision()
        print("precision_ok", digest)
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
