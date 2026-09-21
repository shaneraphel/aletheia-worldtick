import pytest
from mcap_channels.store import CHANNELS, register


def test_requires_key():
    CHANNELS.clear()
    with pytest.raises(ValueError):
        register('/imu/data')


def test_binds_key():
    CHANNELS.clear()
    register('/imu/data', mcap_id='m-a')
    register('/lidar/points', mcap_id='m-b')
    assert [row["topic"] for row in CHANNELS["m-a"]] == ["/imu/data"]
    assert [row["topic"] for row in CHANNELS["m-b"]] == ["/lidar/points"]
