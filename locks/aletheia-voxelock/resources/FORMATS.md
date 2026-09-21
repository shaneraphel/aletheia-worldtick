# What an autonomous-driving resource is

A lidar resource reads or writes a scan. KITTI velodyne is little-endian
float32 `x,y,z,intensity`. An empty bin refuses.

```bash
python3.12 show_kitti.py
```

nuScenes instance translations are the box interchange. An empty sample refuses.

```bash
python3.12 show_nusc.py
python3.12 show_nuscenes.py
```

Official-shaped tables live in `resources/synthetic/nuscenes/v1.0-aletheia/`.
`NuScenes()` loads them after a map row with `log_tokens` and `maps/aletheia.png`.
`sample_data` now has thirteen key frames: `LIDAR_TOP`, `LIDAR_FRONT`, `LIDAR_BACK`, `RADAR_FRONT`,
`RADAR_BACK`, `RADAR_LEFT`, and `RADAR_RIGHT` (18-field PCD plus one
pad byte), `CAM_FRONT`, `CAM_BACK`, `CAM_FRONT_LEFT`,
`CAM_FRONT_RIGHT`, `CAM_BACK_LEFT`, and `CAM_BACK_RIGHT`. Official
empty lidar is 0 points. Official empty JPEG or radar raises. A missing
version folder raises. The instance tape refuses an empty sample.

KITTI OXTS copies Accel ax/ay/az, Gyro wx/wy/wz, and Orient
roll/pitch/yaw into the 30-field IMU row. Accel three-vectors become
`ego_pose` `ep1` and `ep2` translations. Orient becomes those
quaternions. Mag three-vectors become `calibrated_sensor` translations
on `MAGNETOMETER`. Mag heading `atan2(my, mx)` becomes those
quaternions. `LIDAR_FRONT` and `LIDAR_BACK` cite those poses. An
empty IMU or empty magnetometer refuses.

Official `NuScenesCanBus` reads `can_bus/scene-0001_*.json`. Steer copies
the XDF CAN first channel. `ms_imu` linear_accel copies Accel.
`vehicle_monitor` copies steer, speed, and the int16 CanId stream.
`zoe_veh_info` copies the four-channel Wheel stream as FL/FR/RL/RR rpm.
`zoesensors` copies the three-channel Pedal stream as brake/steering/throttle.
An empty CAN bus directory, empty wheels, or empty pedals raises.
