import pytest
from sandbox_jobs.store import JOBS, enqueue


def test_requires_isolate():
    JOBS.clear()
    with pytest.raises(ValueError):
        enqueue("echo")


def test_binds_isolate():
    JOBS.clear()
    enqueue("echo a", isolate_id="iso-a")
    enqueue("echo b", isolate_id="iso-b")
    assert [row["cmd"] for row in JOBS["iso-a"]] == ["echo a"]
    assert [row["cmd"] for row in JOBS["iso-b"]] == ["echo b"]
