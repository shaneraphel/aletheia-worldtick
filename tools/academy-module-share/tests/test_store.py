import pytest
from academy_share.store import SHARES, share


def test_requires_module():
    SHARES.clear()
    with pytest.raises(ValueError):
        share("https://example.test", "note")


def test_binds_module():
    SHARES.clear()
    share("https://a.test", "one", module_id="m1")
    share("https://b.test", "two", module_id="m2")
    assert [row["url"] for row in SHARES["m1"]] == ["https://a.test"]
    assert [row["url"] for row in SHARES["m2"]] == ["https://b.test"]
