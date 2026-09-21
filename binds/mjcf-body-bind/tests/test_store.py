import pytest
from mjcf_bodies.store import BODIES, register


def test_requires_key():
    BODIES.clear()
    with pytest.raises(ValueError):
        register('torso')


def test_binds_key():
    BODIES.clear()
    register('torso', mjcf_id='j-a')
    register('foot', mjcf_id='j-b')
    assert [row["link"] for row in BODIES["j-a"]] == ["torso"]
    assert [row["link"] for row in BODIES["j-b"]] == ["foot"]
