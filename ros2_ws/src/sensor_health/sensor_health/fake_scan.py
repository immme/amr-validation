"""가짜 LaserScan ROS2 노드.

정해진 주기로 LaserScan 메시지를 scan 토픽에 발행한다. header.stamp에는 발행
순간보다 delay_sec(초)만큼 이전 시각을 넣는다. 그래서 이 메시지로 측정한 지연은
delay_sec에 가까워야 하며, 이 값을 정답으로 삼아 지연 측정이 맞는지 확인할 수 있다.

사용법:
    ros2 run sensor_health fake_scan [period_sec] [delay_sec]

    period_sec: 발행 주기(초). 생략하면 0.5초.
    delay_sec: stamp를 발행 순간보다 얼마나 과거로 찍을지(초). 생략하면 0.1초.
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
        # 같은 ROS 시계의 현재 시각에서 delay_sec만큼 뺀 시각을 stamp에 넣는다
        stamp = self.get_clock().now() - Duration(seconds=self.delay_sec)
        msg.header.stamp = stamp.to_msg()
        msg.header.frame_id = 'laser'
        # 지연 측정에는 쓰이지 않는다. 메시지 형식을 채우기 위한 최소한의 값이다
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
