#!/usr/bin/env python3.12
"""Show: I used an XDF aba tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from oxtsocc import read_oxts_accel, read_oxts_gyro, read_oxts_orient
from ukkonen import n_suffix_links
from xdfocc import read_xdf_accel, read_xdf_can, read_xdf_can_id, read_xdf_gyro, read_xdf_heading, read_xdf_mag, read_xdf_markers, read_xdf_orient, read_xdf_samples, read_xdf_pedal, read_xdf_wheel, xdf_occupancy

XDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.xdf"
OXTS = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.oxts"


def theirs() -> dict:
    import pyxdf

    streams, hdr = pyxdf.load_xdf(str(XDF))
    empty = Path("/tmp/aletheia-empty-stem.xdf")
    empty.write_bytes(b"")
    empty_streams = "raised"
    try:
        pyxdf.load_xdf(str(empty))
        empty_streams = "accepted"
    except Exception:
        empty_streams = "raised"
    eeg = next(s for s in streams if s["info"]["name"][0] == "EEG")
    marker = next(s for s in streams if s["info"]["name"][0] == "Marker")
    accel = next(s for s in streams if s["info"]["name"][0] == "Accel")
    gyro = next(s for s in streams if s["info"]["name"][0] == "Gyro")
    orient = next(s for s in streams if s["info"]["name"][0] == "Orient")
    mag = next(s for s in streams if s["info"]["name"][0] == "Mag")
    can = next(s for s in streams if s["info"]["name"][0] == "CAN")
    can_id = next(s for s in streams if s["info"]["name"][0] == "CanId")
    wheel = next(s for s in streams if s["info"]["name"][0] == "Wheel")
    pedal = next(s for s in streams if s["info"]["name"][0] == "Pedal")
    ts = eeg["time_series"]
    return {
        "package": "pyxdf",
        "version": getattr(pyxdf, "__version__", "ok"),
        "n_streams": int(len(streams)),
        "header_streamcount": int(hdr.get("info", {}).get("streamcount", ["0"])[0]),
        "official_samples": [int(x) for x in ts.reshape(-1)],
        "official_markers": [row[0] for row in marker["time_series"]],
        "marker_format": marker["info"]["channel_format"][0],
        "official_accel": [[float(x) for x in row] for row in accel["time_series"]],
        "accel_format": accel["info"]["channel_format"][0],
        "official_gyro": [[float(x) for x in row] for row in gyro["time_series"]],
        "gyro_format": gyro["info"]["channel_format"][0],
        "official_orient": [[float(x) for x in row] for row in orient["time_series"]],
        "orient_format": orient["info"]["channel_format"][0],
        "official_mag": [[float(x) for x in row] for row in mag["time_series"]],
        "mag_format": mag["info"]["channel_format"][0],
        "official_can": [[float(x) for x in row] for row in can["time_series"]],
        "can_format": can["info"]["channel_format"][0],
        "official_can_id": [int(x) for x in can_id["time_series"].reshape(-1)],
        "can_id_format": can_id["info"]["channel_format"][0],
        "official_wheel": [[float(x) for x in row] for row in wheel["time_series"]],
        "wheel_format": wheel["info"]["channel_format"][0],
        "official_pedal": [[float(x) for x in row] for row in pedal["time_series"]],
        "pedal_format": pedal["info"]["channel_format"][0],
        "clock_times": [float(x) for x in eeg["clock_times"]],
        "footer_sample_count": int(eeg.get("footer", {}).get("info", {}).get("sample_count", ["0"])[0]),
        "empty": empty_streams,
    }


def main():
    word = "".join(chr(int(v)) for v in read_xdf_samples(XDF))
    rec = {
        "schema": "stemlock.show_xdf.v1",
        "used": "https://github.com/sccn/xdf",
        "built": "XDF StreamHeader+Samples aba have 3 suffix links; official pyxdf n_streams is 2",
        "theirs": theirs(),
        "ours": {"n": xdf_occupancy(XDF), "word": word, "links": n_suffix_links(word), "markers": read_xdf_markers(XDF), "accel": [list(r) for r in read_xdf_accel(XDF)], "gyro": [list(r) for r in read_xdf_gyro(XDF)], "oxts": [list(r) for r in read_oxts_accel(OXTS)], "oxts_gyro": [list(r) for r in read_oxts_gyro(OXTS)], "orient": [list(r) for r in read_xdf_orient(XDF)], "oxts_orient": [list(r) for r in read_oxts_orient(OXTS)], "mag": [list(r) for r in read_xdf_mag(XDF)], "heading": read_xdf_heading(XDF), "can": [list(r) for r in read_xdf_can(XDF)], "can_id": read_xdf_can_id(XDF), "wheel": [list(r) for r in read_xdf_wheel(XDF)], "pedal": [list(r) for r in read_xdf_pedal(XDF)]},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["links"] != 3 or rec["ours"]["word"] != "aba":
        raise SystemExit("stemlock xdf show identity failed")
    if rec["theirs"]["n_streams"] != 10 or rec["theirs"]["empty"] != "raised":
        raise SystemExit("pyxdf stem identity failed")
    if rec["theirs"]["official_samples"] != [97, 98, 97]:
        raise SystemExit("pyxdf stem samples identity failed")
    if rec["theirs"]["clock_times"] != [0.0]:
        raise SystemExit("pyxdf stem clock identity failed")
    if rec["theirs"]["footer_sample_count"] != 3:
        raise SystemExit("pyxdf stem footer identity failed")
    if rec["theirs"]["marker_format"] != "string" or rec["theirs"]["official_markers"] != ["go", "end"]:
        raise SystemExit("pyxdf stem marker identity failed")
    if rec["ours"]["markers"] != ["go", "end"]:
        raise SystemExit("ours stem marker identity failed")
    if rec["theirs"]["accel_format"] != "float32" or rec["theirs"]["official_accel"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]:
        raise SystemExit("pyxdf stem accel identity failed")
    if rec["ours"]["accel"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]:
        raise SystemExit("ours stem accel identity failed")
    if rec["ours"]["oxts"] != rec["ours"]["accel"]:
        raise SystemExit("ours stem oxts identity failed")
    if rec["theirs"]["gyro_format"] != "float32" or rec["theirs"]["official_gyro"] != [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]:
        raise SystemExit("pyxdf stem gyro identity failed")
    if rec["ours"]["gyro"] != [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]:
        raise SystemExit("ours stem gyro identity failed")
    if rec["ours"]["oxts_gyro"] != rec["ours"]["gyro"]:
        raise SystemExit("ours stem oxts gyro identity failed")
    if rec["theirs"]["orient_format"] != "float32" or rec["theirs"]["official_orient"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]:
        raise SystemExit("pyxdf stem orient identity failed")
    if rec["ours"]["orient"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]:
        raise SystemExit("ours stem orient identity failed")
    if rec["ours"]["oxts_orient"] != rec["ours"]["orient"]:
        raise SystemExit("ours stem oxts orient identity failed")
    if rec["theirs"]["mag_format"] != "float32" or rec["theirs"]["official_mag"] != [[0.25, 0.0, 0.5], [-0.25, 0.0, 0.5]]:
        raise SystemExit("pyxdf stem mag identity failed")
    if rec["ours"]["mag"] != [[0.25, 0.0, 0.5], [-0.25, 0.0, 0.5]]:
        raise SystemExit("ours stem mag identity failed")
    if rec["ours"]["heading"] != [0.0, 3.141592653589793]:
        raise SystemExit("ours stem heading identity failed")
    if rec["theirs"]["can_format"] != "float32" or rec["theirs"]["official_can"] != [[0.25, 1.0, 0.0], [-0.25, 1.0, 0.0]]:
        raise SystemExit("pyxdf stem can identity failed")
    if rec["ours"]["can"] != [[0.25, 1.0, 0.0], [-0.25, 1.0, 0.0]]:
        raise SystemExit("ours stem can identity failed")
    if rec["theirs"]["can_id_format"] != "int16" or rec["theirs"]["official_can_id"] != [256, 512]:
        raise SystemExit("pyxdf stem can id identity failed")
    if rec["ours"]["can_id"] != [256, 512]:
        raise SystemExit("ours stem can id identity failed")
    if rec["theirs"]["wheel_format"] != "float32" or rec["theirs"]["official_wheel"] != [[8.0, 8.0, 8.0, 8.0], [16.0, 16.0, 16.0, 16.0]]:
        raise SystemExit("pyxdf stem wheel identity failed")
    if rec["ours"]["wheel"] != [[8.0, 8.0, 8.0, 8.0], [16.0, 16.0, 16.0, 16.0]]:
        raise SystemExit("ours stem wheel identity failed")
    if rec["theirs"]["pedal_format"] != "float32" or rec["theirs"]["official_pedal"] != [[0.25, 0.25, 0.25], [0.5, 0.1875, 0.375]]:
        raise SystemExit("pyxdf pedal identity failed")
    if rec["ours"]["pedal"] != [[0.25, 0.25, 0.25], [0.5, 0.1875, 0.375]]:
        raise SystemExit("ours pedal identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
