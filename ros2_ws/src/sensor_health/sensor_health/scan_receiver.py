"""scan 토픽의 메시지마다 지연(도착 시각 - header.stamp)을 로그로 남기는 ROS2 노드.

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
        # 도착 시각에서 stamp를 빼므로, stamp를 찍은 쪽과 같은 ROS 시계로 측정한다.
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
