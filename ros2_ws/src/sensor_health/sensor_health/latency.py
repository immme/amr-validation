"""도착 시각과 header.stamp로 메시지의 지연(초)을 계산한다.

도착 시각은 stamp와 같은 시계(ROS 시계)로 측정한 초 단위 숫자여야 한다.
"""


def latency_sec(arrival_sec, stamp_sec, stamp_nanosec):
    """도착 시각에서 header.stamp를 뺀 지연(초)을 돌려준다.

    Args:
        arrival_sec: 메시지가 도착한 시각(초).
        stamp_sec: header.stamp의 sec 값.
        stamp_nanosec: header.stamp의 nanosec 값.

    Returns:
        지연(초). 도착이 stamp보다 앞서면 음수.
    """
    return arrival_sec - (stamp_sec + stamp_nanosec / 1_000_000_000)
