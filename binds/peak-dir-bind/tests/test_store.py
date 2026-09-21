import pytest
from peak_dirs.store import PEAKS, register


def test_requires_key():
    PEAKS.clear()
    with pytest.raises(ValueError):
        register(2)


def test_binds_key():
    PEAKS.clear()
    register(2, peak_id='p-a')
    register(3, peak_id='p-b')
    assert [row["npeak"] for row in PEAKS["p-a"]] == [2]
    assert [row["npeak"] for row in PEAKS["p-b"]] == [3]
