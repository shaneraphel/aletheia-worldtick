#!/usr/bin/env python3.12
"""Show: an MCAP world log (an empty log)."""
from __future__ import annotations
import io, json, platform, sys
from pathlib import Path
from mcapocc import mcap_occupancy, read_mcap
from datalog import datalog_fixpoint

MCAP = Path(__file__).resolve().parent / "resources" / "synthetic" / "world.mcap"


def theirs() -> dict:
    from mcap.writer import Writer
    from mcap.reader import make_reader
    import mcap

    buf = io.BytesIO()
    w = Writer(buf)
    w.start()
    w.finish()
    buf.seek(0)
    n = sum(1 for _ in make_reader(buf).iter_messages())
    return {"package": "mcap", "version": mcap.__version__, "empty_messages": n}


def main():
    samples = read_mcap(MCAP)
    n = len(samples)
    facts = [0]
    edges = [(i, i + 1) for i in range(n - 1)]
    empty = "raised"
    p = Path("/tmp/aletheia-empty.mcap")
    from mcap.writer import Writer

    with p.open("wb") as fh:
        w = Writer(fh)
        w.start()
        w.finish()
    try:
        read_mcap(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "worldtick.show_mcap.v1",
        "used": "https://github.com/foxglove/mcap",
        "built": "three MCAP samples, world reach 3; empty log is absence",
        "theirs": theirs(),
        "ours": {"n": mcap_occupancy(MCAP), "reach": datalog_fixpoint(n, facts, edges), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["reach"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("worldtick mcap show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
