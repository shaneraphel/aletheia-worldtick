# What a dexterous-hand resource is

MuJoCo MJCF names finger sites. An empty model refuses.

```bash
python3.12 show_mjcf.py
```

A MANO-shaped tape stores 16 hand joints. Letter names spell the finger word.
Zero joints refuse.

```bash
python3.12 show_mano.py
```

Official MuJoCo loads the same MJCF. An empty worldbody is accepted there; this kernel refuses empty sites.

```bash
python3.12 show_mujoco.py
```
