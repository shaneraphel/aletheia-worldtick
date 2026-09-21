import pytest
from opencv_vision.store import ACTIONS, register


def test_requires_key():
    ACTIONS.clear()
    with pytest.raises(ValueError):
        register("look")


def test_binds_key():
    ACTIONS.clear()
    register("look", vision_id="v-a")
    register("act", vision_id="v-b")
    assert [row["act"] for row in ACTIONS["v-a"]] == ["look"]
    assert [row["act"] for row in ACTIONS["v-b"]] == ["act"]
