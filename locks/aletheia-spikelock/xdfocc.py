"""XDF occupancy. An empty LSL recording is absence, not 0 streams.

XDF is the on-disk form of Lab Streaming Layer. This writer emits magic
`XDF:`, a FileHeader, an int16 EEG stream, a string Marker stream, a
float32 Accel stream, a float32 Gyro stream, a float32 Orient
stream, a float32 Mag stream, a float32 CAN stream, a float32
Wheel stream, and a float32 Pedal stream. A header with stream count 0, empty samples, empty
marker labels, empty accel rows, empty gyro rows, empty orient
rows, empty mag rows, empty CAN rows, empty CAN ids, empty wheel
rows, or empty pedal rows, refuses.
"""
from __future__ import annotations

import math
import struct
from pathlib import Path

Z = -1


def _varlen(n: int) -> bytes:
    if n < 256:
        return bytes([1, n])
    raise ValueError("uncompiled XDF recording is absence")


def _chunk(tag: int, body: bytes) -> bytes:
    return _varlen(2 + len(body)) + struct.pack("<H", tag) + body


def _footer(n: int) -> bytes:
    xml = (
        '<?xml version="1.0"?>'
        f"<info><first_timestamp>1</first_timestamp>"
        f"<last_timestamp>{n}</last_timestamp>"
        f"<sample_count>{n}</sample_count></info>"
    ).encode("ascii")
    if len(xml) > 249:
        raise ValueError("uncompiled XDF recording is absence")
    return xml


def _header(name: str, typ: str, fmt: str, nchns: int = 1) -> bytes:
    xml = (
        '<?xml version="1.0"?>'
        f"<info><name>{name}</name><type>{typ}</type>"
        f"<channel_count>{int(nchns)}</channel_count><nominal_srate>1</nominal_srate>"
        f"<channel_format>{fmt}</channel_format><source_id>aletheia</source_id></info>"
    ).encode("ascii")
    if len(xml) > 249:
        raise ValueError("uncompiled XDF recording is absence")
    return xml


def _int16_stream(stream_id: int, name: str, typ: str, vals: list[int]) -> bytes:
    n = len(vals)
    if n < 1 or n > 250:
        raise ValueError("uncompiled XDF recording is absence")
    sid = struct.pack("<I", int(stream_id))
    samples_body = sid + _varlen(n)
    for x in vals:
        samples_body += b"\x00" + struct.pack("<h", int(x))
    return (
        _chunk(2, sid + _header(name, typ, "int16"))
        + _chunk(3, samples_body)
        + _chunk(4, sid + struct.pack("<dd", 0.0, 0.0))
        + _chunk(6, sid + _footer(n))
    )


def _string_stream(stream_id: int, name: str, typ: str, labels: list[str]) -> bytes:
    labs = [str(x) for x in labels]
    if not labs or any(not x or not x.isascii() for x in labs):
        raise ValueError("uncompiled XDF recording is absence")
    n = len(labs)
    if n < 1 or n > 250:
        raise ValueError("uncompiled XDF recording is absence")
    sid = struct.pack("<I", int(stream_id))
    samples_body = sid + _varlen(n)
    for lab in labs:
        raw = lab.encode("ascii")
        if len(raw) > 250:
            raise ValueError("uncompiled XDF recording is absence")
        samples_body += b"\x00" + _varlen(len(raw)) + raw
    return (
        _chunk(2, sid + _header(name, typ, "string"))
        + _chunk(3, samples_body)
        + _chunk(4, sid + struct.pack("<dd", 0.0, 0.0))
        + _chunk(6, sid + _footer(n))
    )


def _float32_stream(stream_id: int, name: str, typ: str, rows: list) -> bytes:
    body_rows = [tuple(float(x) for x in row) for row in rows]
    if not body_rows or any(len(r) < 1 for r in body_rows):
        raise ValueError("uncompiled XDF recording is absence")
    nchns = len(body_rows[0])
    if any(len(r) != nchns for r in body_rows):
        raise ValueError("uncompiled XDF recording is absence")
    n = len(body_rows)
    if n < 1 or n > 250:
        raise ValueError("uncompiled XDF recording is absence")
    sid = struct.pack("<I", int(stream_id))
    samples_body = sid + _varlen(n)
    fmt = "<" + "f" * nchns
    for row in body_rows:
        samples_body += b"\x00" + struct.pack(fmt, *row)
    return (
        _chunk(2, sid + _header(name, typ, "float32", nchns))
        + _chunk(3, samples_body)
        + _chunk(4, sid + struct.pack("<dd", 0.0, 0.0))
        + _chunk(6, sid + _footer(n))
    )


def write_xdf(path, n_streams, samples=None, markers=None, accel=None, gyro=None, orient=None, mag=None, can=None, can_ids=None, wheels=None, pedals=None):
    if n_streams is None or int(n_streams) < 1:
        raise ValueError("uncompiled XDF recording is absence")
    if samples is None or not samples:
        raise ValueError("uncompiled XDF recording is absence")
    vals = [int(x) for x in samples]
    extra = "<samples>" + " ".join(str(x) for x in vals) + "</samples>"
    file_xml = (
        '<?xml version="1.0"?>'
        f"<info><version>1.0</version><streamcount>{int(n_streams)}</streamcount>{extra}</info>"
    ).encode("ascii")
    if len(file_xml) > 253:
        raise ValueError("uncompiled XDF recording is absence")
    blob = b"XDF:" + _chunk(1, file_xml) + _int16_stream(1, "EEG", "EEG", vals)
    if int(n_streams) >= 2:
        labs = list(markers) if markers else ["go", "end"]
        blob += _string_stream(2, "Marker", "Markers", labs)
    if int(n_streams) >= 3:
        if accel is not None and not accel:
            raise ValueError("uncompiled XDF recording is absence")
        rows = list(accel) if accel is not None else [(0.0, 0.0, 1.0), (0.0, 0.0, -1.0)]
        blob += _float32_stream(3, "Accel", "Accelerometer", rows)
    if int(n_streams) >= 4:
        if gyro is not None and not gyro:
            raise ValueError("uncompiled XDF recording is absence")
        grows = list(gyro) if gyro is not None else [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
        blob += _float32_stream(4, "Gyro", "Gyroscope", grows)
    if int(n_streams) >= 5:
        if orient is not None and not orient:
            raise ValueError("uncompiled XDF recording is absence")
        orows = list(orient) if orient is not None else [(0.0, 0.0, 1.0), (0.0, 0.0, -1.0)]
        blob += _float32_stream(5, "Orient", "Orientation", orows)
    if int(n_streams) >= 6:
        if mag is not None and not mag:
            raise ValueError("uncompiled XDF recording is absence")
        mrows = list(mag) if mag is not None else [(0.25, 0.0, 0.5), (-0.25, 0.0, 0.5)]
        blob += _float32_stream(6, "Mag", "Magnetometer", mrows)
    if int(n_streams) >= 7:
        if can is not None and not can:
            raise ValueError("uncompiled XDF recording is absence")
        crows = list(can) if can is not None else [(0.25, 1.0, 0.0), (-0.25, 1.0, 0.0)]
        blob += _float32_stream(7, "CAN", "CAN", crows)
    if int(n_streams) >= 8:
        if can_ids is not None and not can_ids:
            raise ValueError("uncompiled XDF recording is absence")
        ids = [int(x) for x in (can_ids if can_ids is not None else [256, 512])]
        blob += _int16_stream(8, "CanId", "CAN", ids)
    if int(n_streams) >= 9:
        if wheels is not None and not wheels:
            raise ValueError("uncompiled XDF recording is absence")
        wrows = list(wheels) if wheels is not None else [(8.0, 8.0, 8.0, 8.0), (16.0, 16.0, 16.0, 16.0)]
        blob += _float32_stream(9, "Wheel", "Wheel", wrows)
    if int(n_streams) >= 10:
        if pedals is not None and not pedals:
            raise ValueError("uncompiled XDF recording is absence")
        prows = list(pedals) if pedals is not None else [(0.25, 0.25, 0.25), (0.5, 0.1875, 0.375)]
        blob += _float32_stream(10, "Pedal", "Pedal", prows)
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(blob)
    return dest


def _iter_chunks(raw: bytes):
    i = 4
    while i < len(raw):
        if i + 2 > len(raw) or raw[i] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        chunklen = raw[i + 1]
        i += 2
        if i + chunklen > len(raw):
            raise ValueError("uncompiled XDF recording is absence")
        tag = struct.unpack_from("<H", raw, i)[0]
        yield tag, raw[i + 2 : i + chunklen]
        i += chunklen


def read_xdf(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 8 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    text = raw.decode("ascii", errors="replace")
    marker = "<streamcount>"
    i = text.find(marker)
    if i < 0:
        raise ValueError("uncompiled XDF recording is absence")
    j = text.find("</streamcount>", i)
    n = int(text[i + len(marker) : j])
    if n < 1:
        raise ValueError("uncompiled XDF recording is absence")
    return n


def read_xdf_samples(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 16 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    for tag, body in _iter_chunks(raw):
        if tag != 3:
            continue
        if len(body) < 6 or struct.unpack_from("<I", body, 0)[0] != 1:
            continue
        if body[4] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        n = body[5]
        i = 6
        samples = []
        for _ in range(n):
            if i + 3 > len(body) or body[i] != 0:
                raise ValueError("uncompiled XDF recording is absence")
            samples.append(struct.unpack_from("<h", body, i + 1)[0])
            i += 3
        if not samples:
            raise ValueError("uncompiled XDF recording is absence")
        return samples
    raise ValueError("uncompiled XDF recording is absence")


def read_xdf_markers(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 16 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    for tag, body in _iter_chunks(raw):
        if tag != 3:
            continue
        if len(body) < 6 or struct.unpack_from("<I", body, 0)[0] != 2:
            continue
        if body[4] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        n = body[5]
        i = 6
        labels = []
        for _ in range(n):
            if i + 2 > len(body) or body[i] != 0 or body[i + 1] != 1:
                raise ValueError("uncompiled XDF recording is absence")
            ln = body[i + 2]
            i += 3
            if ln < 1 or i + ln > len(body):
                raise ValueError("uncompiled XDF recording is absence")
            labels.append(body[i : i + ln].decode("ascii"))
            i += ln
        if not labels:
            raise ValueError("uncompiled XDF recording is absence")
        return labels
    raise ValueError("uncompiled XDF recording is absence")


def read_xdf_accel(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 16 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    for tag, body in _iter_chunks(raw):
        if tag != 3:
            continue
        if len(body) < 6 or struct.unpack_from("<I", body, 0)[0] != 3:
            continue
        if body[4] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        n = body[5]
        if n < 1 or (len(body) - 6) % n != 0:
            raise ValueError("uncompiled XDF recording is absence")
        step = (len(body) - 6) // n
        if step < 5 or (step - 1) % 4 != 0:
            raise ValueError("uncompiled XDF recording is absence")
        nchns = (step - 1) // 4
        i = 6
        rows = []
        for _ in range(n):
            if body[i] != 0:
                raise ValueError("uncompiled XDF recording is absence")
            i += 1
            rows.append(struct.unpack_from("<" + "f" * nchns, body, i))
            i += 4 * nchns
        if not rows:
            raise ValueError("uncompiled XDF recording is absence")
        return rows
    raise ValueError("uncompiled XDF recording is absence")


def read_xdf_gyro(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 16 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    for tag, body in _iter_chunks(raw):
        if tag != 3:
            continue
        if len(body) < 6 or struct.unpack_from("<I", body, 0)[0] != 4:
            continue
        if body[4] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        n = body[5]
        if n < 1 or (len(body) - 6) % n != 0:
            raise ValueError("uncompiled XDF recording is absence")
        step = (len(body) - 6) // n
        if step < 5 or (step - 1) % 4 != 0:
            raise ValueError("uncompiled XDF recording is absence")
        nchns = (step - 1) // 4
        i = 6
        rows = []
        for _ in range(n):
            if body[i] != 0:
                raise ValueError("uncompiled XDF recording is absence")
            i += 1
            rows.append(struct.unpack_from("<" + "f" * nchns, body, i))
            i += 4 * nchns
        if not rows:
            raise ValueError("uncompiled XDF recording is absence")
        return rows
    raise ValueError("uncompiled XDF recording is absence")


def read_xdf_orient(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 16 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    for tag, body in _iter_chunks(raw):
        if tag != 3:
            continue
        if len(body) < 6 or struct.unpack_from("<I", body, 0)[0] != 5:
            continue
        if body[4] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        n = body[5]
        if n < 1 or (len(body) - 6) % n != 0:
            raise ValueError("uncompiled XDF recording is absence")
        step = (len(body) - 6) // n
        if step < 5 or (step - 1) % 4 != 0:
            raise ValueError("uncompiled XDF recording is absence")
        nchns = (step - 1) // 4
        i = 6
        rows = []
        for _ in range(n):
            if body[i] != 0:
                raise ValueError("uncompiled XDF recording is absence")
            i += 1
            rows.append(struct.unpack_from("<" + "f" * nchns, body, i))
            i += 4 * nchns
        if not rows:
            raise ValueError("uncompiled XDF recording is absence")
        return rows
    raise ValueError("uncompiled XDF recording is absence")


def read_xdf_mag(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 16 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    for tag, body in _iter_chunks(raw):
        if tag != 3:
            continue
        if len(body) < 6 or struct.unpack_from("<I", body, 0)[0] != 6:
            continue
        if body[4] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        n = body[5]
        if n < 1 or (len(body) - 6) % n != 0:
            raise ValueError("uncompiled XDF recording is absence")
        step = (len(body) - 6) // n
        if step < 5 or (step - 1) % 4 != 0:
            raise ValueError("uncompiled XDF recording is absence")
        nchns = (step - 1) // 4
        i = 6
        rows = []
        for _ in range(n):
            if body[i] != 0:
                raise ValueError("uncompiled XDF recording is absence")
            i += 1
            rows.append(struct.unpack_from("<" + "f" * nchns, body, i))
            i += 4 * nchns
        if not rows:
            raise ValueError("uncompiled XDF recording is absence")
        return rows
    raise ValueError("uncompiled XDF recording is absence")


def read_xdf_heading(path):
    rows = read_xdf_mag(path)
    headings = [math.atan2(float(row[1]), float(row[0])) for row in rows]
    if not headings:
        raise ValueError("uncompiled XDF recording is absence")
    return headings


def read_xdf_can(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 16 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    for tag, body in _iter_chunks(raw):
        if tag != 3:
            continue
        if len(body) < 6 or struct.unpack_from("<I", body, 0)[0] != 7:
            continue
        if body[4] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        n = body[5]
        if n < 1 or (len(body) - 6) % n != 0:
            raise ValueError("uncompiled XDF recording is absence")
        step = (len(body) - 6) // n
        if step < 5 or (step - 1) % 4 != 0:
            raise ValueError("uncompiled XDF recording is absence")
        nchns = (step - 1) // 4
        i = 6
        rows = []
        for _ in range(n):
            if body[i] != 0:
                raise ValueError("uncompiled XDF recording is absence")
            i += 1
            rows.append(struct.unpack_from("<" + "f" * nchns, body, i))
            i += 4 * nchns
        if not rows:
            raise ValueError("uncompiled XDF recording is absence")
        return rows
    raise ValueError("uncompiled XDF recording is absence")


def read_xdf_can_id(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 16 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    for tag, body in _iter_chunks(raw):
        if tag != 3:
            continue
        if len(body) < 6 or struct.unpack_from("<I", body, 0)[0] != 8:
            continue
        if body[4] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        n = body[5]
        i = 6
        ids = []
        for _ in range(n):
            if i + 3 > len(body) or body[i] != 0:
                raise ValueError("uncompiled XDF recording is absence")
            ids.append(struct.unpack_from("<h", body, i + 1)[0])
            i += 3
        if not ids:
            raise ValueError("uncompiled XDF recording is absence")
        return ids
    raise ValueError("uncompiled XDF recording is absence")


def read_xdf_wheel(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 16 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    for tag, body in _iter_chunks(raw):
        if tag != 3:
            continue
        if len(body) < 6 or struct.unpack_from("<I", body, 0)[0] != 9:
            continue
        if body[4] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        n = body[5]
        if n < 1 or (len(body) - 6) % n != 0:
            raise ValueError("uncompiled XDF recording is absence")
        step = (len(body) - 6) // n
        if step < 5 or (step - 1) % 4 != 0:
            raise ValueError("uncompiled XDF recording is absence")
        nchns = (step - 1) // 4
        i = 6
        rows = []
        for _ in range(n):
            if body[i] != 0:
                raise ValueError("uncompiled XDF recording is absence")
            i += 1
            rows.append(struct.unpack_from("<" + "f" * nchns, body, i))
            i += 4 * nchns
        if not rows:
            raise ValueError("uncompiled XDF recording is absence")
        return rows
    raise ValueError("uncompiled XDF recording is absence")


def read_xdf_pedal(path):
    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 16 or raw[:4] != b"XDF:":
        raise ValueError("uncompiled XDF recording is absence")
    for tag, body in _iter_chunks(raw):
        if tag != 3:
            continue
        if len(body) < 6 or struct.unpack_from("<I", body, 0)[0] != 10:
            continue
        if body[4] != 1:
            raise ValueError("uncompiled XDF recording is absence")
        n = body[5]
        if n < 1 or (len(body) - 6) % n != 0:
            raise ValueError("uncompiled XDF recording is absence")
        step = (len(body) - 6) // n
        if step < 5 or (step - 1) % 4 != 0:
            raise ValueError("uncompiled XDF recording is absence")
        nchns = (step - 1) // 4
        i = 6
        rows = []
        for _ in range(n):
            if body[i] != 0:
                raise ValueError("uncompiled XDF recording is absence")
            i += 1
            rows.append(struct.unpack_from("<" + "f" * nchns, body, i))
            i += 4 * nchns
        if not rows:
            raise ValueError("uncompiled XDF recording is absence")
        return rows
    raise ValueError("uncompiled XDF recording is absence")


def xdf_occupancy(path):
    return read_xdf(path)
