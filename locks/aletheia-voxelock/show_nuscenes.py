#!/usr/bin/env python3.12
"""Show: I used official NuScenes tables, and I refused an empty sample."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from nuscocc import mag_heading, nusc_occupancy, read_nusc_calib_mag, read_nusc_calib_rot, read_nusc_can_imu, read_nusc_can_steer, read_nusc_vehicle_monitor, read_nusc_zoe_sensors, read_nusc_zoe_wheels, rpy_to_quat, read_nusc, read_nusc_camera, read_nusc_ego, read_nusc_ego_rot, read_nusc_lidar, read_nusc_radar, read_nusc_sample_ego
from oxtsocc import read_oxts_accel, read_oxts_gyro, read_oxts_orient
from octpart import octpart_ne

ROOT = Path(__file__).resolve().parent / "resources" / "synthetic"
SAMPLE = ROOT / "sample.json"
TABLES = ROOT / "nuscenes" / "v1.0-aletheia"
DATAROOT = ROOT / "nuscenes"
LIDAR = DATAROOT / "samples" / "LIDAR_TOP" / "aletheia.pcd.bin"
LIDAR_FRONT = DATAROOT / "samples" / "LIDAR_FRONT" / "aletheia.pcd.bin"
LIDAR_BACK = DATAROOT / "samples" / "LIDAR_BACK" / "aletheia.pcd.bin"
CAMERA = DATAROOT / "samples" / "CAM_FRONT" / "aletheia.jpg"
RADAR = DATAROOT / "samples" / "RADAR_FRONT" / "aletheia.pcd"
RADAR_BACK = DATAROOT / "samples" / "RADAR_BACK" / "aletheia.pcd"
RADAR_LEFT = DATAROOT / "samples" / "RADAR_LEFT" / "aletheia.pcd"
RADAR_RIGHT = DATAROOT / "samples" / "RADAR_RIGHT" / "aletheia.pcd"
CAM_BACK = DATAROOT / "samples" / "CAM_BACK" / "aletheia.jpg"
CAM_FL = DATAROOT / "samples" / "CAM_FRONT_LEFT" / "aletheia.jpg"
CAM_FR = DATAROOT / "samples" / "CAM_FRONT_RIGHT" / "aletheia.jpg"
CAM_BL = DATAROOT / "samples" / "CAM_BACK_LEFT" / "aletheia.jpg"
CAM_BR = DATAROOT / "samples" / "CAM_BACK_RIGHT" / "aletheia.jpg"
OXTS = ROOT / "oxts.txt"


def theirs() -> dict:
    from nuscenes.nuscenes import NuScenes
    from nuscenes.utils.data_classes import LidarPointCloud, RadarPointCloud

    nusc = NuScenes(version="v1.0-aletheia", dataroot=str(DATAROOT), verbose=False)
    empty = "raised"
    try:
        NuScenes(version="v1.0-empty", dataroot=str(DATAROOT), verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    trans = [tuple(int(x) for x in a["translation"]) for a in nusc.sample_annotation]
    from PIL import Image

    path = nusc.get_sample_data_path("sd0")
    cloud = LidarPointCloud.from_file(path)
    cam_path = nusc.get_sample_data_path("sd1")
    cam = Image.open(cam_path)
    cam.load()
    empty_lidar = Path("/tmp/aletheia-empty.pcd.bin")
    empty_lidar.write_bytes(b"")
    empty_pts = int(LidarPointCloud.from_file(str(empty_lidar)).nbr_points())
    empty_cam = "raised"
    p = Path("/tmp/aletheia-empty-cam.jpg")
    p.write_bytes(b"")
    try:
        Image.open(p).load()
        empty_cam = "accepted"
    except Exception:
        empty_cam = "raised"
    from nuscenes.can_bus.can_bus_api import NuScenesCanBus

    empty_can = "raised"
    try:
        NuScenesCanBus(dataroot="/tmp/aletheia-empty-can-root")
        empty_can = "accepted"
    except Exception:
        empty_can = "raised"
    nusc_can = NuScenesCanBus(dataroot=str(DATAROOT))
    return {
        "package": "nuscenes-devkit",
        "status": "loaded",
        "n_annotation": int(len(nusc.sample_annotation)),
        "n_sample_data": int(len(nusc.sample_data)),
        "lidar_channel": nusc.get("sample", "s0")["data"].get("LIDAR_TOP"),
        "lidar_front": nusc.get("sample", "s0")["data"].get("LIDAR_FRONT"),
        "lidar_back": nusc.get("sample", "s0")["data"].get("LIDAR_BACK"),
        "camera_channel": nusc.get("sample", "s0")["data"].get("CAM_FRONT"),
        "radar_channel": nusc.get("sample", "s0")["data"].get("RADAR_FRONT"),
        "radar_back": nusc.get("sample", "s0")["data"].get("RADAR_BACK"),
        "radar_left": nusc.get("sample", "s0")["data"].get("RADAR_LEFT"),
        "radar_right": nusc.get("sample", "s0")["data"].get("RADAR_RIGHT"),
        "cam_back": nusc.get("sample", "s0")["data"].get("CAM_BACK"),
        "cam_front_left": nusc.get("sample", "s0")["data"].get("CAM_FRONT_LEFT"),
        "cam_front_right": nusc.get("sample", "s0")["data"].get("CAM_FRONT_RIGHT"),
        "cam_back_left": nusc.get("sample", "s0")["data"].get("CAM_BACK_LEFT"),
        "cam_back_right": nusc.get("sample", "s0")["data"].get("CAM_BACK_RIGHT"),
        "lidar_points": int(cloud.nbr_points()),
        "lidar_front_points": int(LidarPointCloud.from_file(nusc.get_sample_data_path("sd11")).nbr_points()),
        "lidar_back_points": int(LidarPointCloud.from_file(nusc.get_sample_data_path("sd12")).nbr_points()),
        "radar_points": int(RadarPointCloud.from_file(nusc.get_sample_data_path("sd2")).nbr_points()),
        "radar_back_points": int(RadarPointCloud.from_file(nusc.get_sample_data_path("sd5")).nbr_points()),
        "radar_left_points": int(RadarPointCloud.from_file(nusc.get_sample_data_path("sd6")).nbr_points()),
        "radar_right_points": int(RadarPointCloud.from_file(nusc.get_sample_data_path("sd7")).nbr_points()),
        "camera_size": [int(cam.size[0]), int(cam.size[1])],
        "empty_lidar_points": empty_pts,
        "empty_camera": empty_cam,
        "translations": trans,
        "empty_version": empty,
        "n_ego_pose": int(len(nusc.ego_pose)),
        "ego_accel": [nusc.get("ego_pose", "ep1")["translation"], nusc.get("ego_pose", "ep2")["translation"]],
        "lidar_front_ego": nusc.get("sample_data", "sd11")["ego_pose_token"],
        "lidar_back_ego": nusc.get("sample_data", "sd12")["ego_pose_token"],
        "ego_rot": [nusc.get("ego_pose", "ep1")["rotation"], nusc.get("ego_pose", "ep2")["rotation"]],
        "n_calibrated_sensor": int(len(nusc.calibrated_sensor)),
        "mag_channel": nusc.get("sensor", "mag")["channel"],
        "mag_calib": [nusc.get("calibrated_sensor", "csm0")["translation"], nusc.get("calibrated_sensor", "csm1")["translation"]],
        "mag_calib_rot": [nusc.get("calibrated_sensor", "csm0")["rotation"], nusc.get("calibrated_sensor", "csm1")["rotation"]],
        "can_steer": [float(m["value"]) for m in nusc_can.get_messages("scene-0001", "steeranglefeedback")],
        "can_imu": [m["linear_accel"] for m in nusc_can.get_messages("scene-0001", "ms_imu")],
        "can_pose": [m["pos"] for m in nusc_can.get_messages("scene-0001", "pose")],
        "empty_can": empty_can,
        "vm_steer": [float(m["steering"]) for m in nusc_can.get_messages("scene-0001", "vehicle_monitor")],
        "vm_speed": [float(m["vehicle_speed"]) for m in nusc_can.get_messages("scene-0001", "vehicle_monitor")],
        "vm_can_id": [int(m["can_id"]) for m in nusc_can.get_messages("scene-0001", "vehicle_monitor")],
        "zoe_fl": [float(m["FL_wheel_speed"]) for m in nusc_can.get_messages("scene-0001", "zoe_veh_info")],
        "zoe_wheels": [
            [float(m["FL_wheel_speed"]), float(m["FR_wheel_speed"]), float(m["RL_wheel_speed"]), float(m["RR_wheel_speed"])]
            for m in nusc_can.get_messages("scene-0001", "zoe_veh_info")
        ],
        "zoe_brake": [float(m["brake_sensor"]) for m in nusc_can.get_messages("scene-0001", "zoesensors")],
        "zoe_sensors": [
            [float(m["brake_sensor"]), float(m["steering_sensor"]), float(m["throttle_sensor"])]
            for m in nusc_can.get_messages("scene-0001", "zoesensors")
        ],
    }


def main():
    pts = read_nusc(SAMPLE)
    table_pts = read_nusc(TABLES)
    lidar_pts = read_nusc_lidar(LIDAR)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-nusc.json")
    p.write_text("{}\n")
    try:
        read_nusc(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_lidar = "raised"
    q = Path("/tmp/aletheia-empty-ours.pcd.bin")
    q.write_bytes(b"")
    try:
        read_nusc_lidar(q)
        empty_lidar = "accepted"
    except ValueError:
        empty_lidar = "raised"
    empty_cam = "raised"
    r = Path("/tmp/aletheia-empty-ours-cam.jpg")
    r.write_bytes(b"")
    try:
        read_nusc_camera(r)
        empty_cam = "accepted"
    except ValueError:
        empty_cam = "raised"
    empty_radar = "raised"
    s = Path("/tmp/aletheia-empty-ours.pcd")
    s.write_bytes(b"")
    try:
        read_nusc_radar(s)
        empty_radar = "accepted"
    except ValueError:
        empty_radar = "raised"
    radar_pts = read_nusc_radar(RADAR)
    rec = {
        "schema": "voxelock.show_nuscenes.v1",
        "used": "https://github.com/nutonomy/nuscenes-devkit",
        "built": "official zoesensors brake/steering/throttle copy the Pedal stream; empty pedals are absence",
        "theirs": theirs(),
        "ours": {
            "n": nusc_occupancy(SAMPLE),
            "table_n": nusc_occupancy(TABLES),
            "lidar_n": len(lidar_pts),
            "lidar_front_n": len(read_nusc_lidar(LIDAR_FRONT)),
            "lidar_back_n": len(read_nusc_lidar(LIDAR_BACK)),
            "ne": octpart_ne(pts, 1, 1, 1),
            "table_ne": octpart_ne(table_pts, 1, 1, 1),
            "lidar_ne": octpart_ne(lidar_pts, 1, 1, 1),
            "empty": empty,
            "empty_lidar": empty_lidar,
            "camera": read_nusc_camera(CAMERA),
            "empty_camera": empty_cam,
            "radar_n": len(radar_pts),
            "radar_ne": octpart_ne(radar_pts, 1, 1, 1),
            "radar_back_n": len(read_nusc_radar(RADAR_BACK)),
            "radar_left_n": len(read_nusc_radar(RADAR_LEFT)),
            "radar_right_n": len(read_nusc_radar(RADAR_RIGHT)),
            "empty_radar": empty_radar,
            "cam_back": read_nusc_camera(CAM_BACK)["width"],
            "cam_front_left": read_nusc_camera(CAM_FL)["width"],
            "cam_front_right": read_nusc_camera(CAM_FR)["width"],
            "cam_back_left": read_nusc_camera(CAM_BL)["width"],
            "cam_back_right": read_nusc_camera(CAM_BR)["width"],
            "oxts": [list(r) for r in read_oxts_accel(OXTS)],
            "oxts_gyro": [list(r) for r in read_oxts_gyro(OXTS)],
            "ego": [list(r) for r in read_nusc_ego(TABLES)],
            "sample_ego": [list(r) for r in read_nusc_sample_ego(TABLES)],
            "oxts_orient": [list(r) for r in read_oxts_orient(OXTS)],
            "ego_rot": [list(r) for r in read_nusc_ego_rot(TABLES)],
            "calib_mag": [list(r) for r in read_nusc_calib_mag(TABLES)],
            "calib_rot": [list(r) for r in read_nusc_calib_rot(TABLES)],
            "can_steer": read_nusc_can_steer(DATAROOT),
            "can_imu": [list(r) for r in read_nusc_can_imu(DATAROOT)],
            "vehicle_monitor": [list(r) for r in read_nusc_vehicle_monitor(DATAROOT)],
            "zoe_wheels": [list(r) for r in read_nusc_zoe_wheels(DATAROOT)],
            "zoe_sensors": [list(r) for r in read_nusc_zoe_sensors(DATAROOT)],
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["ne"] != 1 or rec["ours"]["lidar_ne"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("voxelock nuscenes show identity failed")
    if rec["ours"]["empty_lidar"] != "raised":
        raise SystemExit("voxelock empty lidar identity failed")
    if rec["ours"]["empty_camera"] != "raised" or rec["ours"]["camera"]["width"] != 8:
        raise SystemExit("voxelock empty camera identity failed")
    if rec["ours"]["empty_radar"] != "raised" or rec["ours"]["radar_ne"] != 1:
        raise SystemExit("voxelock radar identity failed")
    if rec["theirs"]["n_annotation"] != 2 or rec["theirs"]["n_sample_data"] != 13:
        raise SystemExit("official NuScenes identity failed")
    if rec["theirs"]["radar_channel"] != "sd2" or rec["theirs"]["radar_points"] != 2:
        raise SystemExit("official radar identity failed")
    if rec["theirs"]["radar_back"] != "sd5" or rec["theirs"]["radar_back_points"] != 2:
        raise SystemExit("official radar back identity failed")
    if rec["theirs"]["radar_left"] != "sd6" or rec["theirs"]["radar_left_points"] != 2:
        raise SystemExit("official radar left identity failed")
    if rec["theirs"]["radar_right"] != "sd7" or rec["theirs"]["radar_right_points"] != 2:
        raise SystemExit("official radar right identity failed")
    if rec["ours"]["radar_back_n"] != 2 or rec["ours"]["radar_left_n"] != 2 or rec["ours"]["radar_right_n"] != 2:
        raise SystemExit("ours radar side identity failed")
    if rec["theirs"]["cam_back"] != "sd3" or rec["theirs"]["cam_front_left"] != "sd4":
        raise SystemExit("official extra camera identity failed")
    if rec["theirs"]["cam_front_right"] != "sd8" or rec["ours"]["cam_front_right"] != 8:
        raise SystemExit("official front-right camera identity failed")
    if rec["theirs"]["cam_back_left"] != "sd9" or rec["ours"]["cam_back_left"] != 8:
        raise SystemExit("official back-left camera identity failed")
    if rec["theirs"]["cam_back_right"] != "sd10" or rec["ours"]["cam_back_right"] != 8:
        raise SystemExit("official back-right camera identity failed")
    if rec["theirs"]["camera_channel"] != "sd1" or rec["theirs"]["empty_camera"] != "raised":
        raise SystemExit("official camera identity failed")
    if rec["theirs"]["lidar_points"] != 2 or rec["theirs"]["empty_lidar_points"] != 0:
        raise SystemExit("official lidar identity failed")
    if rec["theirs"]["lidar_front"] != "sd11" or rec["theirs"]["lidar_front_points"] != 2:
        raise SystemExit("official lidar front identity failed")
    if rec["ours"]["lidar_front_n"] != 2:
        raise SystemExit("ours lidar front identity failed")
    if rec["theirs"]["lidar_back"] != "sd12" or rec["theirs"]["lidar_back_points"] != 2:
        raise SystemExit("official lidar back identity failed")
    if rec["ours"]["lidar_back_n"] != 2:
        raise SystemExit("ours lidar back identity failed")
    if rec["theirs"]["translations"] != [(0, 0, 0), (2, 2, 2)]:
        raise SystemExit("official NuScenes translation identity failed")
    if rec["theirs"]["n_ego_pose"] != 3 or rec["theirs"]["ego_accel"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]:
        raise SystemExit("official ego pose accel identity failed")
    if rec["ours"]["oxts"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]] or rec["ours"]["ego"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]:
        raise SystemExit("ours oxts ego identity failed")
    if rec["theirs"]["lidar_front_ego"] != "ep1" or rec["theirs"]["lidar_back_ego"] != "ep2":
        raise SystemExit("official sample ego pose identity failed")
    if rec["ours"]["sample_ego"] != [["sd11", "ep1"], ["sd12", "ep2"]]:
        raise SystemExit("ours sample ego pose identity failed")
    if rec["ours"]["oxts_gyro"] != [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]:
        raise SystemExit("ours oxts gyro identity failed")
    expect_rot = [list(rpy_to_quat(0.0, 0.0, 1.0)), list(rpy_to_quat(0.0, 0.0, -1.0))]
    if rec["theirs"]["ego_rot"] != expect_rot:
        raise SystemExit("official ego rotation identity failed")
    if rec["ours"]["ego_rot"] != expect_rot or rec["ours"]["oxts_orient"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]:
        raise SystemExit("ours oxts orient identity failed")
    if rec["theirs"]["mag_channel"] != "MAGNETOMETER" or rec["theirs"]["n_calibrated_sensor"] != 15:
        raise SystemExit("official mag sensor identity failed")
    if rec["theirs"]["mag_calib"] != [[0.25, 0.0, 0.5], [-0.25, 0.0, 0.5]]:
        raise SystemExit("official mag calib identity failed")
    if rec["ours"]["calib_mag"] != [[0.25, 0.0, 0.5], [-0.25, 0.0, 0.5]]:
        raise SystemExit("ours mag calib identity failed")
    expect_heading_rot = [
        list(rpy_to_quat(0.0, 0.0, mag_heading((0.25, 0.0, 0.5)))),
        list(rpy_to_quat(0.0, 0.0, mag_heading((-0.25, 0.0, 0.5)))),
    ]
    if rec["theirs"]["mag_calib_rot"] != expect_heading_rot:
        raise SystemExit("official mag heading rotation identity failed")
    if rec["ours"]["calib_rot"] != expect_heading_rot:
        raise SystemExit("ours mag heading rotation identity failed")
    if rec["theirs"]["empty_can"] != "raised":
        raise SystemExit("official empty can bus identity failed")
    if rec["theirs"]["can_steer"] != [0.25, -0.25] or rec["ours"]["can_steer"] != [0.25, -0.25]:
        raise SystemExit("official can steer identity failed")
    if rec["theirs"]["can_imu"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]] or rec["ours"]["can_imu"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]:
        raise SystemExit("official can imu identity failed")
    if rec["theirs"]["can_pose"] != [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]:
        raise SystemExit("official can pose identity failed")
    if rec["theirs"]["vm_steer"] != [0.25, -0.25] or rec["theirs"]["vm_speed"] != [1.0, 1.0]:
        raise SystemExit("official vehicle monitor identity failed")
    if rec["theirs"]["vm_can_id"] != [256, 512] or rec["ours"]["vehicle_monitor"] != [[0.25, 1.0, 256], [-0.25, 1.0, 512]]:
        raise SystemExit("official vehicle monitor can id identity failed")
    if rec["theirs"]["zoe_fl"] != [8.0, 16.0] or rec["theirs"]["zoe_wheels"] != [[8.0, 8.0, 8.0, 8.0], [16.0, 16.0, 16.0, 16.0]]:
        raise SystemExit("official zoe wheel identity failed")
    if rec["ours"]["zoe_wheels"] != [[8.0, 8.0, 8.0, 8.0], [16.0, 16.0, 16.0, 16.0]]:
        raise SystemExit("ours zoe wheel identity failed")
    if rec["theirs"]["zoe_brake"] != [0.25, 0.5] or rec["theirs"]["zoe_sensors"] != [[0.25, 0.25, 0.25], [0.5, 0.1875, 0.375]]:
        raise SystemExit("official zoe sensor identity failed")
    if rec["ours"]["zoe_sensors"] != [[0.25, 0.25, 0.25], [0.5, 0.1875, 0.375]]:
        raise SystemExit("ours zoe sensor identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
