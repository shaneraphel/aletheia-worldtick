import pytest
from alexa_intents.store import UTTERANCES, register


def test_requires_key():
    UTTERANCES.clear()
    with pytest.raises(ValueError):
        register("hello")


def test_binds_key():
    UTTERANCES.clear()
    register("hello", intent_id="i-a")
    register("bye", intent_id="i-b")
    assert [row["text"] for row in UTTERANCES["i-a"]] == ["hello"]
    assert [row["text"] for row in UTTERANCES["i-b"]] == ["bye"]
