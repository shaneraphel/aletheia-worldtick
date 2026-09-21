import pytest
from orc_stripes.store import STRIPES, register


def test_requires_key():
    STRIPES.clear()
    with pytest.raises(ValueError):
        register('r0')


def test_binds_key():
    STRIPES.clear()
    register('r0', orc_id='o-a')
    register('r1', orc_id='o-b')
    assert [row["rid"] for row in STRIPES["o-a"]] == ['r0']
    assert [row["rid"] for row in STRIPES["o-b"]] == ['r1']
