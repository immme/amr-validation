"""도착 시각과 header.stamp로 메시지의 지연(초)을 계산한다.

ROS2 노드와 분리해 두어 pytest만으로 검사할 수 있다. 도착 시각은 stamp와 같은
시계(ROS 시계)로 잰 초 단위 숫자여야 한다.
"""


def latency_sec(arrival_sec, stamp_sec, stamp_nanosec):
    """지연(초)을 돌려준다.

    arrival_sec: 메시지가 도착한 시각(초)
    stamp_sec, stamp_nanosec: header.stamp의 sec, nanosec 칸의 값
    """
    return arrival_sec - (stamp_sec + stamp_nanosec / 1_000_000_000)
