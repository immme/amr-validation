"""센서 메시지의 마지막 도착 시각을 기억하고 경과 시간을 계산한다.

시각은 호출하는 쪽이 같은 시계로 측정한 초 단위 숫자로 넘긴다.
"""


class ArrivalTracker:
    def __init__(self):
        self.last_time = None

    def on_arrival(self, now):
        self.last_time = now

    def age(self, now):
        """마지막 도착 뒤 지난 시간(초)을 돌려준다. 아직 받지 못했으면 None."""
        if self.last_time is None:
            return None
        return now - self.last_time
