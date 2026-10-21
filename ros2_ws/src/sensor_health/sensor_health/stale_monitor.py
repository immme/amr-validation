"""scan 토픽의 메시지가 끊겼는지 감시해 /diagnostics에 상태를 발행하는 ROS2 노드.

사용법:
    ros2 run sensor_health stale_monitor
    ros2 run sensor_health stale_monitor --ros-args -p timeout_sec:=3.0 -p check_period_sec:=0.5

    timeout_sec: 이 시간(초) 이상 새 메시지가 없으면 STALE. 기본 2.0. 실행 중에 바꾸면
        다음 판정부터 반영된다.
    check_period_sec: 판정해서 상태를 발행하는 주기(초). 기본 0.5. 시작할 때만 읽는다.
"""

import rclpy
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_health.stale_check import is_stale
from sensor_msgs.msg import LaserScan

STATUS_NAME = 'stale_monitor: scan'


class StaleMonitor(Node):
    def __init__(self):
        super().__init__('stale_monitor')
        self.declare_parameter('timeout_sec', 2.0)
        self.declare_parameter('check_period_sec', 0.5)

        self.last_arrival_ns = None
        self.last_stale = None

        # 센서 드라이버는 보통 best_effort로 발행한다. 센서용 QoS로 구독해야
        # reliable과 best_effort 발행자 모두와 연결된다.
        self.sub = self.create_subscription(
            LaserScan, 'scan', self.on_scan, qos_profile_sensor_data)
        self.pub = self.create_publisher(DiagnosticArray, '/diagnostics', 10)

        check_period_sec = self.get_parameter('check_period_sec').value
        self.timer = self.create_timer(check_period_sec, self.on_check)
        self.get_logger().info(
            f'monitoring scan, publishing /diagnostics every {check_period_sec}s')

    def on_scan(self, msg):
        self.last_arrival_ns = self.get_clock().now().nanoseconds

    def on_check(self):
        # 실행 중에 바꾼 timeout_sec이 다음 판정부터 반영되도록 판정할 때마다 읽는다.
        timeout_sec = self.get_parameter('timeout_sec').value
        timeout_ns = round(timeout_sec * 1_000_000_000)
        now = self.get_clock().now()
        stale = is_stale(now.nanoseconds, self.last_arrival_ns, timeout_ns)

        status = DiagnosticStatus()
        status.name = STATUS_NAME
        if stale:
            status.level = DiagnosticStatus.STALE
            if self.last_arrival_ns is None:
                status.message = 'no message received yet'
            else:
                status.message = f'no message for {timeout_sec}s or more'
        else:
            status.level = DiagnosticStatus.OK
            status.message = 'receiving'

        array = DiagnosticArray()
        array.header.stamp = now.to_msg()
        array.status.append(status)
        self.pub.publish(array)

        # 상태가 바뀔 때만 로그를 남겨 0.5초마다 같은 줄이 쌓이지 않게 한다.
        if stale != self.last_stale:
            if stale:
                self.get_logger().warn(f'scan STALE: {status.message}')
            else:
                self.get_logger().info('scan OK')
            self.last_stale = stale


def main(args=None):
    rclpy.init(args=args)
    node = StaleMonitor()
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
