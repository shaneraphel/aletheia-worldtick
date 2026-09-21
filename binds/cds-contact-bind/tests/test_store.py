import pytest
from cds_contacts.store import MESSAGES, register


def test_requires_key():
    MESSAGES.clear()
    with pytest.raises(ValueError):
        register("hello")


def test_binds_key():
    MESSAGES.clear()
    register("hello", contact_id="c-a")
    register("bye", contact_id="c-b")
    assert [row["text"] for row in MESSAGES["c-a"]] == ["hello"]
    assert [row["text"] for row in MESSAGES["c-b"]] == ["bye"]
