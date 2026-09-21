import pytest
from rosbag_topics.store import TOPICS, register


def test_requires_key():
    TOPICS.clear()
    with pytest.raises(ValueError):
        register('/scan')


def test_binds_key():
    TOPICS.clear()
    register('/scan', bag_id='b-a')
    register('/odom', bag_id='b-b')
    assert [row["name"] for row in TOPICS["b-a"]] == ['/scan']
    assert [row["name"] for row in TOPICS["b-b"]] == ['/odom']
