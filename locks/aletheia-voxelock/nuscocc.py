"""nuScenes occupancy. An empty sample is absence, not 0 boxes.

nuScenes instance translations are the lidar-box interchange. Zero
translations refuse.
"""
from __future__ import annotations

import json
from pathlib import Path

Z = -1


def write_nusc(path, points):
    if points is None or not points:
        raise ValueError("uncompiled nuScenes sample is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    inst = []
    for i, (x, y, z) in enumerate(points):
        inst.append({"token": f"i{i}", "translation": [float(x), float(y), float(z)]})
    dest.write_text(json.dumps({"instance": inst}, indent=2) + "\n")
    return dest


def _points_from_rows(rows):
    pts = []
    if not isinstance(rows, list):
        return pts
    for row in rows:
        if not isinstance(row, dict):
            continue
        t = row.get("translation")
        if not t or len(t) < 3:
            continue
        pts.append((int(t[0]), int(t[1]), int(t[2])))
    return pts


def read_nusc(path):
    dest = Path(path)
    if dest.is_dir():
        for name in ("sample_annotation.json", "instance.json"):
            cand = dest / name
            if not cand.exists():
                continue
            try:
                rows = json.loads(cand.read_text())
            except json.JSONDecodeError as exc:
                raise ValueError("uncompiled nuScenes sample is absence") from exc
            pts = _points_from_rows(rows)
            if pts:
                return pts
        raise ValueError("uncompiled nuScenes sample is absence")
    text = dest.read_text() if dest.exists() else ""
    if not text.strip():
        raise ValueError("uncompiled nuScenes sample is absence")
    try:
        rec = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes sample is absence") from exc
    if isinstance(rec, list):
        pts = _points_from_rows(rec)
        if not pts:
            raise ValueError("uncompiled nuScenes sample is absence")
        return pts
    inst = rec.get("instance") if isinstance(rec, dict) else None
    if inst:
        pts = _points_from_rows(inst)
        if pts:
            return pts
    ann = rec.get("sample_annotation") if isinstance(rec, dict) else None
    pts = _points_from_rows(ann)
    if not pts:
        raise ValueError("uncompiled nuScenes sample is absence")
    return pts


def write_nusc_lidar(path, points):
    """Five little-endian float32 words: x,y,z,intensity,ring. Official LidarPointCloud reshapes (-1, 5)."""
    if points is None or not points:
        raise ValueError("uncompiled nuScenes lidar is absence")
    import struct

    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    blob = b""
    for row in points:
        x, y, z = float(row[0]), float(row[1]), float(row[2])
        inten = float(row[3]) if len(row) > 3 else 1.0
        ring = float(row[4]) if len(row) > 4 else 0.0
        blob += struct.pack("<fffff", x, y, z, inten, ring)
    dest.write_bytes(blob)
    return dest


def read_nusc_lidar(path):
    import struct

    raw = Path(path).read_bytes() if Path(path).exists() else b""
    if len(raw) < 20 or len(raw) % 20 != 0:
        raise ValueError("uncompiled nuScenes lidar is absence")
    pts = []
    for i in range(len(raw) // 20):
        x, y, z, inten, ring = struct.unpack_from("<fffff", raw, 20 * i)
        pts.append((int(x), int(y), int(z)))
    if not pts:
        raise ValueError("uncompiled nuScenes lidar is absence")
    return pts


def write_nusc_camera(path, *, size=(8, 8), color=(255, 128, 0)):
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    from PIL import Image

    img = Image.new("RGB", size, color)
    img.save(dest, format="JPEG")
    return dest


def read_nusc_camera(path):
    dest = Path(path)
    if not dest.exists() or dest.stat().st_size < 16:
        raise ValueError("uncompiled nuScenes camera is absence")
    from PIL import Image

    try:
        img = Image.open(dest)
        img.load()
    except Exception as exc:
        raise ValueError("uncompiled nuScenes camera is absence") from exc
    w, h = img.size
    if w < 1 or h < 1:
        raise ValueError("uncompiled nuScenes camera is absence")
    return {"width": int(w), "height": int(h), "mode": img.mode}


def write_nusc_radar(path, points):
    """nuScenes radar PCD v0.7 binary. Official RadarPointCloud requires 18 fields and one pad byte."""
    if points is None or not points:
        raise ValueError("uncompiled nuScenes radar is absence")
    import struct

    n = len(points)
    header = (
        "# .PCD v0.7 - Point Cloud Data file format\n"
        "VERSION 0.7\n"
        "FIELDS x y z dyn_prop id rcs vx vy vx_comp vy_comp is_quality_valid ambig_state x_rms y_rms invalid_state pdh0 vx_rms vy_rms\n"
        "SIZE 4 4 4 1 2 4 4 4 4 4 1 1 1 1 1 1 1 1\n"
        "TYPE F F F I I F F F F F I I I I I I I I\n"
        "COUNT 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n"
        f"WIDTH {n}\n"
        "HEIGHT 1\n"
        "VIEWPOINT 0 0 0 1 0 0 0\n"
        f"POINTS {n}\n"
        "DATA binary\n"
    ).encode("ascii")
    blob = b""
    for i, row in enumerate(points):
        x, y, z = float(row[0]), float(row[1]), float(row[2])
        # dyn_prop=0, ambig_state=3, invalid_state=0 so default official filters keep the point
        blob += struct.pack("<fffbhfffffbbbbbbbb", x, y, z, 0, i, 1.0, 0.0, 0.0, 0.0, 0.0, 1, 3, 0, 0, 0, 1, 0, 0)
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(header + blob + b"\x00")
    return dest


def read_nusc_radar(path):
    dest = Path(path)
    raw = dest.read_bytes() if dest.exists() else b""
    if b"DATA binary" not in raw or b"POINTS 0" in raw:
        raise ValueError("uncompiled nuScenes radar is absence")
    start = raw.find(b"DATA binary\n")
    if start < 0:
        raise ValueError("uncompiled nuScenes radar is absence")
    data = raw[start + len(b"DATA binary\n") :]
    rec_size = 43
    if len(data) < rec_size:
        raise ValueError("uncompiled nuScenes radar is absence")
    import struct

    n = len(data) // rec_size
    pts = []
    for i in range(n):
        x, y, z = struct.unpack_from("<fff", data, i * rec_size)[:3]
        pts.append((int(x), int(y), int(z)))
    if not pts:
        raise ValueError("uncompiled nuScenes radar is absence")
    return pts


def rpy_to_quat(roll, pitch, yaw):
    import math

    cr, sr = math.cos(float(roll) / 2.0), math.sin(float(roll) / 2.0)
    cp, sp = math.cos(float(pitch) / 2.0), math.sin(float(pitch) / 2.0)
    cy, sy = math.cos(float(yaw) / 2.0), math.sin(float(yaw) / 2.0)
    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy
    return (qw, qx, qy, qz)


def write_nusc_ego_from_accel(table_dir, accels, orients=None):
    if accels is None or not accels:
        raise ValueError("uncompiled nuScenes ego pose is absence")
    if orients is not None and not orients:
        raise ValueError("uncompiled nuScenes ego pose is absence")
    dest = Path(table_dir) / "ego_pose.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    poses = [
        {
            "token": "ep0",
            "timestamp": 0,
            "rotation": [1.0, 0.0, 0.0, 0.0],
            "translation": [0.0, 0.0, 0.0],
        }
    ]
    for i, row in enumerate(accels):
        if row is None or len(row) < 3:
            raise ValueError("uncompiled nuScenes ego pose is absence")
        x, y, z = float(row[0]), float(row[1]), float(row[2])
        rot = [1.0, 0.0, 0.0, 0.0]
        if orients is not None:
            orow = orients[i] if i < len(orients) else None
            if orow is None or len(orow) < 3:
                raise ValueError("uncompiled nuScenes ego pose is absence")
            rot = [float(v) for v in rpy_to_quat(orow[0], orow[1], orow[2])]
        poses.append(
            {
                "token": f"ep{i + 1}",
                "timestamp": i + 1,
                "rotation": rot,
                "translation": [x, y, z],
            }
        )
    dest.write_text(json.dumps(poses, indent=2) + "\n")
    return dest


def read_nusc_ego(table_dir):
    dest = Path(table_dir) / "ego_pose.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes ego pose is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes ego pose is absence") from exc
    pts = []
    for row in rows:
        if not isinstance(row, dict) or row.get("token") == "ep0":
            continue
        t = row.get("translation")
        if not t or len(t) < 3:
            continue
        pts.append((float(t[0]), float(t[1]), float(t[2])))
    if not pts:
        raise ValueError("uncompiled nuScenes ego pose is absence")
    return pts


def read_nusc_ego_rot(table_dir):
    dest = Path(table_dir) / "ego_pose.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes ego pose is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes ego pose is absence") from exc
    quats = []
    for row in rows:
        if not isinstance(row, dict) or row.get("token") == "ep0":
            continue
        r = row.get("rotation")
        if not r or len(r) < 4:
            continue
        quats.append((float(r[0]), float(r[1]), float(r[2]), float(r[3])))
    if not quats:
        raise ValueError("uncompiled nuScenes ego pose is absence")
    return quats


def write_nusc_sample_ego(table_dir, mapping):
    if mapping is None or not mapping:
        raise ValueError("uncompiled nuScenes sample ego pose is absence")
    dest = Path(table_dir) / "sample_data.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes sample ego pose is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes sample ego pose is absence") from exc
    if not isinstance(rows, list) or not rows:
        raise ValueError("uncompiled nuScenes sample ego pose is absence")
    by_tok = {row.get("token"): row for row in rows if isinstance(row, dict)}
    for item in mapping:
        if item is None or len(item) < 2:
            raise ValueError("uncompiled nuScenes sample ego pose is absence")
        sd_tok, ep_tok = str(item[0]), str(item[1])
        if not sd_tok or not ep_tok or sd_tok not in by_tok:
            raise ValueError("uncompiled nuScenes sample ego pose is absence")
        by_tok[sd_tok]["ego_pose_token"] = ep_tok
        if ep_tok.startswith("ep") and ep_tok[2:].isdigit():
            by_tok[sd_tok]["timestamp"] = int(ep_tok[2:])
    dest.write_text(json.dumps(rows, indent=2) + "\n")
    return dest


def read_nusc_sample_ego(table_dir):
    dest = Path(table_dir) / "sample_data.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes sample ego pose is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes sample ego pose is absence") from exc
    pairs = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        tok = row.get("token")
        ep = row.get("ego_pose_token")
        if not tok or not ep or ep == "ep0":
            continue
        pairs.append((str(tok), str(ep)))
    if not pairs:
        raise ValueError("uncompiled nuScenes sample ego pose is absence")
    return pairs


def mag_heading(row):
    import math

    if row is None or len(row) < 2:
        raise ValueError("uncompiled nuScenes calibrated sensor is absence")
    return math.atan2(float(row[1]), float(row[0]))


def write_nusc_calib_from_mag(table_dir, mags):
    if mags is None or not mags:
        raise ValueError("uncompiled nuScenes calibrated sensor is absence")
    table = Path(table_dir)
    sensor_dest = table / "sensor.json"
    calib_dest = table / "calibrated_sensor.json"
    if not sensor_dest.exists() or not calib_dest.exists():
        raise ValueError("uncompiled nuScenes calibrated sensor is absence")
    try:
        sensors = json.loads(sensor_dest.read_text())
        calibs = json.loads(calib_dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes calibrated sensor is absence") from exc
    if not isinstance(sensors, list) or not isinstance(calibs, list):
        raise ValueError("uncompiled nuScenes calibrated sensor is absence")
    if not any(isinstance(row, dict) and row.get("token") == "mag" for row in sensors):
        sensors.append({"token": "mag", "channel": "MAGNETOMETER", "modality": "imu"})
    kept = [row for row in calibs if isinstance(row, dict) and not str(row.get("token", "")).startswith("csm")]
    for i, row in enumerate(mags):
        if row is None or len(row) < 3:
            raise ValueError("uncompiled nuScenes calibrated sensor is absence")
        heading = mag_heading(row)
        kept.append(
            {
                "token": f"csm{i}",
                "sensor_token": "mag",
                "translation": [float(row[0]), float(row[1]), float(row[2])],
                "rotation": [float(v) for v in rpy_to_quat(0.0, 0.0, heading)],
                "camera_intrinsic": [],
            }
        )
    sensor_dest.write_text(json.dumps(sensors, indent=2) + "\n")
    calib_dest.write_text(json.dumps(kept, indent=2) + "\n")
    return calib_dest


def read_nusc_calib_mag(table_dir):
    dest = Path(table_dir) / "calibrated_sensor.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes calibrated sensor is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes calibrated sensor is absence") from exc
    pts = []
    for row in rows:
        if not isinstance(row, dict) or row.get("sensor_token") != "mag":
            continue
        t = row.get("translation")
        if not t or len(t) < 3:
            continue
        pts.append((float(t[0]), float(t[1]), float(t[2])))
    if not pts:
        raise ValueError("uncompiled nuScenes calibrated sensor is absence")
    return pts


def read_nusc_calib_rot(table_dir):
    dest = Path(table_dir) / "calibrated_sensor.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes calibrated sensor is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes calibrated sensor is absence") from exc
    quats = []
    for row in rows:
        if not isinstance(row, dict) or row.get("sensor_token") != "mag":
            continue
        r = row.get("rotation")
        if not r or len(r) < 4:
            continue
        quats.append((float(r[0]), float(r[1]), float(r[2]), float(r[3])))
    if not quats:
        raise ValueError("uncompiled nuScenes calibrated sensor is absence")
    return quats


def write_nusc_can_bus(dataroot, cans, accels=None, gyros=None, orients=None, can_ids=None, wheels=None, pedals=None, scene="scene-0001"):
    if cans is None or not cans:
        raise ValueError("uncompiled nuScenes can bus is absence")
    if accels is not None and not accels:
        raise ValueError("uncompiled nuScenes can bus is absence")
    if gyros is not None and not gyros:
        raise ValueError("uncompiled nuScenes can bus is absence")
    if orients is not None and not orients:
        raise ValueError("uncompiled nuScenes can bus is absence")
    if can_ids is not None and not can_ids:
        raise ValueError("uncompiled nuScenes can bus is absence")
    if wheels is not None and not wheels:
        raise ValueError("uncompiled nuScenes can bus is absence")
    if pedals is not None and not pedals:
        raise ValueError("uncompiled nuScenes can bus is absence")
    if not scene or not str(scene).startswith("scene-"):
        raise ValueError("uncompiled nuScenes can bus is absence")
    accels = list(accels) if accels is not None else [(0.0, 0.0, 1.0), (0.0, 0.0, -1.0)]
    gyros = list(gyros) if gyros is not None else [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    orients = list(orients) if orients is not None else [(0.0, 0.0, 1.0), (0.0, 0.0, -1.0)]
    can_ids = [int(x) for x in can_ids] if can_ids is not None else [256, 512]
    wheels = list(wheels) if wheels is not None else [(8.0, 8.0, 8.0, 8.0), (16.0, 16.0, 16.0, 16.0)]
    pedals = list(pedals) if pedals is not None else [(0.25, 0.25, 0.25), (0.5, 0.1875, 0.375)]
    n = len(cans)
    if n < 1 or len(accels) != n or len(gyros) != n or len(orients) != n or len(can_ids) != n or len(wheels) != n or len(pedals) != n:
        raise ValueError("uncompiled nuScenes can bus is absence")
    dest = Path(dataroot) / "can_bus"
    dest.mkdir(parents=True, exist_ok=True)
    imu = []
    poses = []
    steers = []
    monitors = []
    zoe = []
    sensors = []
    route = []
    for i, crow in enumerate(cans):
        if crow is None or len(crow) < 1:
            raise ValueError("uncompiled nuScenes can bus is absence")
        if accels[i] is None or len(accels[i]) < 3:
            raise ValueError("uncompiled nuScenes can bus is absence")
        if gyros[i] is None or len(gyros[i]) < 3:
            raise ValueError("uncompiled nuScenes can bus is absence")
        if orients[i] is None or len(orients[i]) < 3:
            raise ValueError("uncompiled nuScenes can bus is absence")
        ax, ay, az = float(accels[i][0]), float(accels[i][1]), float(accels[i][2])
        wx, wy, wz = float(gyros[i][0]), float(gyros[i][1]), float(gyros[i][2])
        quat = [float(v) for v in rpy_to_quat(orients[i][0], orients[i][1], orients[i][2])]
        steer = float(crow[0])
        speed = float(crow[1]) if len(crow) > 1 else 0.0
        utime = i + 1
        imu.append({"utime": utime, "linear_accel": [ax, ay, az], "rotation_rate": [wx, wy, wz], "q": quat})
        poses.append(
            {
                "utime": utime,
                "pos": [ax, ay, az],
                "orientation": quat,
                "accel": [ax, ay, az],
                "rotation_rate": [wx, wy, wz],
                "vel": [speed, 0.0, 0.0],
            }
        )
        steers.append({"utime": utime, "value": steer})
        monitors.append(
            {
                "utime": utime,
                "steering": steer,
                "vehicle_speed": speed,
                "yaw_rate": float(crow[2]) if len(crow) > 2 else 0.0,
                "can_id": int(can_ids[i]),
                "gear_position": 7,
                "brake": 0,
                "throttle": 0,
            }
        )
        if wheels[i] is None or len(wheels[i]) < 4:
            raise ValueError("uncompiled nuScenes can bus is absence")
        fl, fr, rl, rr = (float(wheels[i][0]), float(wheels[i][1]), float(wheels[i][2]), float(wheels[i][3]))
        zoe.append(
            {
                "utime": utime,
                "FL_wheel_speed": fl,
                "FR_wheel_speed": fr,
                "RL_wheel_speed": rl,
                "RR_wheel_speed": rr,
                "odom_speed": speed,
            }
        )
        if pedals[i] is None or len(pedals[i]) < 3:
            raise ValueError("uncompiled nuScenes can bus is absence")
        brake, steer_s, throttle = (float(pedals[i][0]), float(pedals[i][1]), float(pedals[i][2]))
        sensors.append(
            {
                "utime": utime,
                "brake_sensor": brake,
                "steering_sensor": steer_s,
                "throttle_sensor": throttle,
            }
        )
        route.append([ax, ay])
    meta = {
        "ms_imu": {"n": n},
        "pose": {"n": n},
        "steeranglefeedback": {"n": n},
        "vehicle_monitor": {"n": n},
        "zoe_veh_info": {"n": n},
        "zoesensors": {"n": n},
        "route": {"n": n},
    }
    (dest / f"{scene}_ms_imu.json").write_text(json.dumps(imu, indent=2) + "\n")
    (dest / f"{scene}_pose.json").write_text(json.dumps(poses, indent=2) + "\n")
    (dest / f"{scene}_steeranglefeedback.json").write_text(json.dumps(steers, indent=2) + "\n")
    (dest / f"{scene}_vehicle_monitor.json").write_text(json.dumps(monitors, indent=2) + "\n")
    (dest / f"{scene}_zoe_veh_info.json").write_text(json.dumps(zoe, indent=2) + "\n")
    (dest / f"{scene}_zoesensors.json").write_text(json.dumps(sensors, indent=2) + "\n")
    (dest / f"{scene}_route.json").write_text(json.dumps(route, indent=2) + "\n")
    (dest / f"{scene}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    return dest


def read_nusc_can_steer(dataroot, scene="scene-0001"):
    dest = Path(dataroot) / "can_bus" / f"{scene}_steeranglefeedback.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes can bus is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes can bus is absence") from exc
    vals = []
    for row in rows:
        if not isinstance(row, dict) or "value" not in row:
            continue
        vals.append(float(row["value"]))
    if not vals:
        raise ValueError("uncompiled nuScenes can bus is absence")
    return vals


def read_nusc_can_imu(dataroot, scene="scene-0001"):
    dest = Path(dataroot) / "can_bus" / f"{scene}_ms_imu.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes can bus is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes can bus is absence") from exc
    accels = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        a = row.get("linear_accel")
        if not a or len(a) < 3:
            continue
        accels.append((float(a[0]), float(a[1]), float(a[2])))
    if not accels:
        raise ValueError("uncompiled nuScenes can bus is absence")
    return accels


def read_nusc_vehicle_monitor(dataroot, scene="scene-0001"):
    dest = Path(dataroot) / "can_bus" / f"{scene}_vehicle_monitor.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes can bus is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes can bus is absence") from exc
    recs = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if "steering" not in row or "vehicle_speed" not in row or "can_id" not in row:
            continue
        recs.append((float(row["steering"]), float(row["vehicle_speed"]), int(row["can_id"])))
    if not recs:
        raise ValueError("uncompiled nuScenes can bus is absence")
    return recs


def read_nusc_zoe_wheels(dataroot, scene="scene-0001"):
    dest = Path(dataroot) / "can_bus" / f"{scene}_zoe_veh_info.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes can bus is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes can bus is absence") from exc
    recs = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        keys = ("FL_wheel_speed", "FR_wheel_speed", "RL_wheel_speed", "RR_wheel_speed")
        if any(k not in row for k in keys):
            continue
        recs.append(tuple(float(row[k]) for k in keys))
    if not recs:
        raise ValueError("uncompiled nuScenes can bus is absence")
    return recs


def read_nusc_zoe_sensors(dataroot, scene="scene-0001"):
    dest = Path(dataroot) / "can_bus" / f"{scene}_zoesensors.json"
    if not dest.exists():
        raise ValueError("uncompiled nuScenes can bus is absence")
    try:
        rows = json.loads(dest.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled nuScenes can bus is absence") from exc
    recs = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        keys = ("brake_sensor", "steering_sensor", "throttle_sensor")
        if any(k not in row for k in keys):
            continue
        recs.append(tuple(float(row[k]) for k in keys))
    if not recs:
        raise ValueError("uncompiled nuScenes can bus is absence")
    return recs


def nusc_occupancy(path):
    return len(read_nusc(path))

