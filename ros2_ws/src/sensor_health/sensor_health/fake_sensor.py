"""0부터 1씩 늘어나는 Int32를 sensor_value 토픽에 발행하는 가짜 센서 ROS2 노드.

사용법:
    ros2 run sensor_health fake_sensor [period_sec]

    period_sec: 발행 주기(초). 기본 0.5.
"""

import sys

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int32

DEFAULT_PERIOD_SEC = 0.5


class FakeSensor(Node):
    def __init__(self, period_sec):
        super().__init__('fake_sensor')
        self.pub = self.create_publisher(Int32, 'sensor_value', 10)
        self.count = 0
        self.timer = self.create_timer(period_sec, self.on_timer)
        self.get_logger().info(
            f'publishing Int32 on sensor_value every {period_sec}s')

    def on_timer(self):
        msg = Int32()
        msg.data = self.count
        self.pub.publish(msg)
        self.count += 1


def main(args=None):
    period_sec = DEFAULT_PERIOD_SEC
    if len(sys.argv) > 1:
        period_sec = float(sys.argv[1])

    rclpy.init(args=args)
    node = FakeSensor(period_sec)
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
