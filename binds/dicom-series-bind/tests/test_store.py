import pytest
from dicom_series.store import SERIES, register


def test_requires_key():
    SERIES.clear()
    with pytest.raises(ValueError):
        register('1.2.3')


def test_binds_key():
    SERIES.clear()
    register('1.2.3', dicom_id='d-a')
    register('1.2.4', dicom_id='d-b')
    assert [row["sop"] for row in SERIES["d-a"]] == ['1.2.3']
    assert [row["sop"] for row in SERIES["d-b"]] == ['1.2.4']
