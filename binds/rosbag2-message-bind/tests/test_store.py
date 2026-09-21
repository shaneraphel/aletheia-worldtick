import pytest
from rosbag2_messages.store import MESSAGES, register


def test_requires_key():
    MESSAGES.clear()
    with pytest.raises(ValueError):
        register('sensor_msgs/msg/Image')


def test_binds_key():
    MESSAGES.clear()
    register('sensor_msgs/msg/Image', bag2_id='b-a')
    register('nav_msgs/msg/Odometry', bag2_id='b-b')
    assert [row["typ"] for row in MESSAGES["b-a"]] == ['sensor_msgs/msg/Image']
    assert [row["typ"] for row in MESSAGES["b-b"]] == ['nav_msgs/msg/Odometry']
