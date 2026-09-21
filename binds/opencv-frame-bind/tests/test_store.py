import pytest
from opencv_frames.store import FRAMES, register


def test_requires_key():
    FRAMES.clear()
    with pytest.raises(ValueError):
        register("x")


def test_binds_key():
    FRAMES.clear()
    register("a", camera_id="cam-a")
    register("b", camera_id="cam-b")
    assert [row["frame"] for row in FRAMES["cam-a"]] == ["a"]
    assert [row["frame"] for row in FRAMES["cam-b"]] == ["b"]
