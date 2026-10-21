"""LaserScan을 scan 토픽에 발행하는 가짜 센서 ROS2 노드.

header.stamp를 발행 순간보다 delay_sec만큼 이전으로 찍는다. 받는 쪽에서 측정한 지연을
delay_sec과 비교해 지연 측정이 맞는지 확인하는 데 쓴다.

사용법:
    ros2 run sensor_health fake_scan [period_sec] [delay_sec]

    period_sec: 발행 주기(초). 기본 0.5.
    delay_sec: stamp를 발행 순간보다 이전으로 찍을 시간(초). 기본 0.1. 음수면 이후로 찍는다.
"""

import sys

import rclpy
from rclpy.duration import Duration
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

DEFAULT_PERIOD_SEC = 0.5
DEFAULT_DELAY_SEC = 0.1


class FakeScan(Node):
    def __init__(self, period_sec, delay_sec):
        super().__init__('fake_scan')
        self.delay_sec = delay_sec
        self.pub = self.create_publisher(LaserScan, 'scan', 10)
        self.timer = self.create_timer(period_sec, self.on_timer)
        self.get_logger().info(
            f'publishing LaserScan on scan every {period_sec}s '
            f'with stamp {delay_sec}s in the past')

    def on_timer(self):
        msg = LaserScan()
        stamp = self.get_clock().now() - Duration(seconds=self.delay_sec)
        msg.header.stamp = stamp.to_msg()
        msg.header.frame_id = 'laser'
        # 지연 측정에는 쓰지 않는 값이다. 메시지 형식을 채우는 최소한의 값만 넣는다.
        msg.angle_min = -0.1
        msg.angle_max = 0.1
        msg.angle_increment = 0.1
        msg.range_min = 0.1
        msg.range_max = 10.0
        msg.ranges = [1.0, 1.0, 1.0]
        self.pub.publish(msg)


def main(args=None):
    period_sec = DEFAULT_PERIOD_SEC
    delay_sec = DEFAULT_DELAY_SEC
    if len(sys.argv) > 1:
        period_sec = float(sys.argv[1])
    if len(sys.argv) > 2:
        delay_sec = float(sys.argv[2])

    rclpy.init(args=args)
    node = FakeScan(period_sec, delay_sec)
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
