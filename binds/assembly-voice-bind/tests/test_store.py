import pytest
from assembly_voice.store import CLIPS, register


def test_requires_key():
    CLIPS.clear()
    with pytest.raises(ValueError):
        register("clip-a")


def test_binds_key():
    CLIPS.clear()
    register("clip-a", voice_id="v-a")
    register("clip-b", voice_id="v-b")
    assert [row["audio"] for row in CLIPS["v-a"]] == ["clip-a"]
    assert [row["audio"] for row in CLIPS["v-b"]] == ["clip-b"]
