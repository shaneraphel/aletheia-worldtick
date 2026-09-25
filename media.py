"""Empty sound, empty picture, empty cloud.

A world-model frame, a bilateral sound file, and a hand scan are
objects these libraries will construct even when nothing was measured.
The session does not read that object as rest, as calm, or as a
finished grasp.

Versions below are the ones measured on this machine. The standard
library wave check does not need them.
"""
from __future__ import annotations

import io
import json
import platform
import sys
import wave
from pathlib import Path

from decode import neural_class

ROOT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parent
TONE = [1, 0, 2, 0, 1, 0, 3, 0]


def wave_frames(samples: list[int], rate: int = 8000) -> int:
    raw = io.BytesIO()
    with wave.open(raw, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(b"".join(int(s).to_bytes(2, "little", signed=True) for s in samples))
    raw.seek(0)
    with wave.open(raw, "rb") as handle:
        return handle.getnframes()


def optional() -> dict:
    rows: dict[str, dict] = {}
    try:
        import numpy as np
        import scipy
        import scipy.io.wavfile as wavfile
    except ImportError:
        rows["scipy"] = {"present": False}
    else:
        raw = io.BytesIO()
        wavfile.write(raw, 8000, np.zeros(0, dtype=np.int16))
        raw.seek(0)
        rate, data = wavfile.read(raw)
        rows["scipy"] = {
            "present": True,
            "version": scipy.__version__,
            "empty_rate": int(rate),
            "empty_shape": list(data.shape),
        }
    try:
        import soundfile as sf
        import numpy as np
    except ImportError:
        rows["soundfile"] = {"present": False}
    else:
        raw = io.BytesIO()
        sf.write(raw, np.zeros(0), 8000, format="WAV")
        raw.seek(0)
        audio, rate = sf.read(raw)
        rows["soundfile"] = {
            "present": True,
            "version": sf.__version__,
            "empty_rate": int(rate),
            "empty_length": int(len(audio)),
        }
    try:
        from PIL import Image
    except ImportError:
        rows["pillow"] = {"present": False}
    else:
        blank = Image.new("RGB", (0, 0))
        rows["pillow"] = {
            "present": True,
            "version": Image.__version__,
            "empty_size": list(blank.size),
            "empty_mode": blank.mode,
        }
    try:
        import cv2
        import numpy as np
    except ImportError:
        rows["opencv"] = {"present": False}
    else:
        empty = np.zeros((0, 0), dtype=np.uint8)
        rows["opencv"] = {
            "present": True,
            "version": cv2.__version__,
            "empty_nonzero": int(cv2.countNonZero(empty)),
        }
    try:
        import open3d as o3d
    except ImportError:
        rows["open3d"] = {"present": False}
    else:
        cloud = o3d.geometry.PointCloud()
        mesh = o3d.geometry.TriangleMesh()
        rows["open3d"] = {
            "present": True,
            "version": o3d.__version__,
            "empty_points": int(len(cloud.points)),
            "empty_has_points": bool(cloud.has_points()),
            "empty_vertices": int(len(mesh.vertices)),
        }
    return rows


def run() -> dict:
    rows = optional()
    return {
        "schema": "worldtick.media.v1",
        "wave_empty_frames": wave_frames([]),
        "wave_tone_frames": wave_frames(TONE),
        "tone_class": neural_class(TONE),
        "libraries": rows,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 900), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    draw.text((36, 24), "Empty media  ·  空的声音、空白画面、空点云", font=small, fill=(139, 148, 158))
    draw.text((36, 64), "这些库会交出一个对象。会话不把它读成静息或抓取完成。", font=title, fill=(230, 237, 243))
    draw.text((36, 112), "These libraries return an object. The session does not read it as rest or as a finished grasp.", font=small, fill=(139, 148, 158))
    lines = [
        ("wave", f"0 frames in a legal file; the 8-sample tone is class {rec['tone_class']}"),
        ("SciPy / soundfile", "an empty array at 8,000 Hz"),
        ("Pillow", "a 0×0 RGB image"),
        ("OpenCV", "count of nonzero pixels in an empty image is 0"),
        ("Open3D", "a cloud with 0 points and a mesh with 0 vertices"),
    ]
    y = 180
    for name, text in lines:
        draw.rounded_rectangle((36, y, 1640, y + 110), radius=14, fill=(22, 27, 34), outline=(48, 54, 61), width=2)
        draw.text((60, y + 18), name, font=body, fill=(121, 192, 255))
        draw.text((60, y + 58), text, font=small, fill=(230, 237, 243))
        y += 128
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if rec["wave_empty_frames"] != 0 or rec["wave_tone_frames"] != 8 or rec["tone_class"] != 1:
        raise SystemExit("wave identity moved")
    try:
        neural_class([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty samples were accepted")
    libs = rec["libraries"]
    expect = {
        "scipy": {"empty_rate": 8000, "empty_shape": [0]},
        "soundfile": {"empty_rate": 8000, "empty_length": 0},
        "pillow": {"empty_size": [0, 0], "empty_mode": "RGB"},
        "opencv": {"empty_nonzero": 0},
        "open3d": {"empty_points": 0, "empty_has_points": False, "empty_vertices": 0},
    }
    for name, fields in expect.items():
        row = libs.get(name, {"present": False})
        if not row.get("present"):
            continue
        for key, value in fields.items():
            if row.get(key) != value:
                raise SystemExit(f"{name} {key} moved: {row.get(key)}")
    figure(rec, ROOT / "docs" / "figures" / "media.png")
    out = ROOT / "results" / "MEDIA.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
