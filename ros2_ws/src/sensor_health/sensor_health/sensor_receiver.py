"""sensor_value 토픽의 메시지 도착 시각을 기록하는 ROS2 노드.

사용법:
    ros2 run sensor_health sensor_receiver
"""

import time

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_health.arrival_tracker import ArrivalTracker
from std_msgs.msg import Int32


class SensorReceiver(Node):
    def __init__(self):
        super().__init__('sensor_receiver')
        self.tracker = ArrivalTracker()
        self.sub = self.create_subscription(
            Int32, 'sensor_value', self.on_msg, 10)
        self.get_logger().info('waiting for Int32 on sensor_value')

    def on_msg(self, msg):
        # 시스템 시계가 바뀌어도 거꾸로 가지 않는 단조 시계로 도착 시각(초)을 측정한다.
        self.tracker.on_arrival(time.monotonic())
        self.get_logger().info(f'received {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = SensorReceiver()
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
