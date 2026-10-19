"""센서 메시지의 마지막 도착 시각을 기억하는 클래스.

ROS2 노드와 분리해 두어 pytest만으로 검사할 수 있다. 시각(now)은 호출하는 쪽이
초 단위 숫자로 넘기며, 같은 시계(예: time.monotonic())의 값만 써야 한다.
"""


class ArrivalTracker:
    def __init__(self):
        self.last_time = None

    def on_arrival(self, now):
        self.last_time = now

    def age(self, now):
        if self.last_time is None:
            return None
        return now - self.last_time
