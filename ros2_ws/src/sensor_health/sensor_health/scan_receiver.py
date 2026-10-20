"""scan 토픽을 구독해 메시지마다 지연을 로그로 남기는 ROS2 노드.

지연은 도착 시각에서 header.stamp를 뺀 값이다. 도착 시각은 stamp를 찍은 쪽과
같은 ROS 시계로 잰다. 계산은 latency 모듈의 latency_sec 함수가 맡고, 이 노드는
메시지를 받아 값을 넘기는 역할만 한다.

사용법:
    ros2 run sensor_health scan_receiver
"""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_health.latency import latency_sec
from sensor_msgs.msg import LaserScan


class ScanReceiver(Node):
    def __init__(self):
        super().__init__('scan_receiver')
        self.sub = self.create_subscription(
            LaserScan, 'scan', self.on_scan, 10)
        self.get_logger().info('waiting for LaserScan on scan')

    def on_scan(self, msg):
        # stamp와 같은 ROS 시계로 도착 시각(초)을 잰다
        arrival_sec = self.get_clock().now().nanoseconds / 1_000_000_000
        delay = latency_sec(
            arrival_sec, msg.header.stamp.sec, msg.header.stamp.nanosec)
        self.get_logger().info(f'latency {delay:.3f} s')


def main(args=None):
    rclpy.init(args=args)
    node = ScanReceiver()
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
