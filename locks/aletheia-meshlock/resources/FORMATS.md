# What a contact-mesh resource is

PCL / Open3D ASCII PCD stores contact sites. POINTS 0 refuses.

```bash
python3.12 show_pcd.py
```

Official Open3D loads the same PCD. An empty `PointCloud` has 0 points; this kernel refuses POINTS 0.

```bash
python3.12 show_open3d.py
```
