import pytest
from avro_blocks.store import BLOCKS, register


def test_requires_key():
    BLOCKS.clear()
    with pytest.raises(ValueError):
        register('10')


def test_binds_key():
    BLOCKS.clear()
    register('10', avro_id='v-a')
    register('20', avro_id='v-b')
    assert [row["nrec"] for row in BLOCKS["v-a"]] == ['10']
    assert [row["nrec"] for row in BLOCKS["v-b"]] == ['20']
