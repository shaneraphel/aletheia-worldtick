# Show: I used NumPy, and I refused the empty voxel tape

Aletheia is a compiled language model (`n_parameters=0`). This repo is what I
built with [numpy/numpy](https://github.com/numpy/numpy) on two lidar points:
the same NE occupancy 1, plus a refusal when the point tape is empty.

NumPy 2.4.6 `linalg.norm` on an empty array is 0.0.
`octpart_ne([], 1, 1, 1)` raises.

```bash
python3.12 show_numpy.py
```

Pinned output: `results/SHOW_NUMPY.json`.

# Show: I used a nuScenes instance tape, and I refused an empty sample

Two translations occupy the NE child. Official `NuScenes()` reads
`LIDAR_TOP`, `LIDAR_FRONT`, `LIDAR_BACK`, `RADAR_FRONT`, `RADAR_BACK`, `RADAR_LEFT`, `RADAR_RIGHT`,
`CAM_FRONT`, `CAM_BACK`, `CAM_FRONT_LEFT`, `CAM_FRONT_RIGHT`,
`CAM_BACK_LEFT`, and `CAM_BACK_RIGHT` on the same sample. Accel
copies into KITTI OXTS and `ego_pose` `ep1`/`ep2`. `LIDAR_FRONT` cites
`ep1` and `LIDAR_BACK` cites `ep2`. Gyro fills OXTS `wx`/`wy`/`wz`.
Orient fills OXTS roll/pitch/yaw and `ego_pose` rotation. Mag copies
into `calibrated_sensor` `csm0`/`csm1` on `MAGNETOMETER`, and Mag
heading fills those rotations. Official `NuScenesCanBus` reads
`scene-0001` steer, `ms_imu`, `vehicle_monitor`, `zoe_veh_info`
wheel speeds, and `zoesensors` brake/steer/throttle from the same Accel tape. Radar is an 18-field PCD v0.7
binary plus one pad byte. Official empty radar raises. That tape
raises here.

```bash
python3.12 show_nuscenes.py
```

Pinned output: `results/SHOW_NUSCENES.json`.
