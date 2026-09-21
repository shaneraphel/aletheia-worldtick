# What a dexterous-hand resource is

This kernel **ingests** an MJCF numeric cost tape (`resources/synthetic/grasp.xml`).
An empty custom table refuses.

```bash
python3.12 show_mjcf.py
python3.12 show_mujoco.py
```

A MANO-shaped tape stores 16 hand joints as MIT JSON. The MPI model weights
are not in this repo. Zero joints refuse.

```bash
python3.12 show_mano.py
```
