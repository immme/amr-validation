"""메시지가 끊겼는지(STALE) 판정한다.

시각은 같은 시계로 측정한 나노초 정수로 받는다. 실수(float)로 계산하면 경계값에서
결과가 어긋날 수 있다.
"""


def is_stale(now_ns, last_arrival_ns, timeout_ns):
    """마지막 도착 뒤 timeout 이상 지났거나 아직 받지 못했으면 STALE로 판정한다.

    Args:
        now_ns: 판정하는 시각(나노초).
        last_arrival_ns: 마지막 메시지가 도착한 시각(나노초). 아직 받지 못했으면 None.
        timeout_ns: STALE로 보는 기준 시간(나노초).

    Returns:
        STALE이면 True, OK면 False.
    """
    if last_arrival_ns is None:
        return True

    if now_ns - last_arrival_ns >= timeout_ns:
        return True
    return False
