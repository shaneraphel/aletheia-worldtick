import pytest
from opencv_cool.store import PIXELS, register


def test_requires_key():
    PIXELS.clear()
    with pytest.raises(ValueError):
        register("tile-a")


def test_binds_key():
    PIXELS.clear()
    register("tile-a", graviton_id="g-a")
    register("tile-b", graviton_id="g-b")
    assert [row["tile"] for row in PIXELS["g-a"]] == ["tile-a"]
    assert [row["tile"] for row in PIXELS["g-b"]] == ["tile-b"]
