import pytest
from bob_reports.store import REPORTS, register


def test_requires_key():
    REPORTS.clear()
    with pytest.raises(ValueError):
        register("note-a")


def test_binds_key():
    REPORTS.clear()
    register("note-a", bob_id="b-a")
    register("note-b", bob_id="b-b")
    assert [row["note"] for row in REPORTS["b-a"]] == ["note-a"]
    assert [row["note"] for row in REPORTS["b-b"]] == ["note-b"]
