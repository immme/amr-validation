import pytest

from sensor_health.arrival_tracker import ArrivalTracker


@pytest.fixture
def tracker():
    return ArrivalTracker()


def test_no_arrival_time_before_first_message(tracker):
    # 요구: 메시지를 받기 전에는 도착 시각이 없다.
    # 행동: 없음(새로 만든 tracker 그대로)
    # 기대:
    assert tracker.last_time is None


def test_arrival_time_is_recorded(tracker):
    # 요구: 메시지가 오면 그 시각이 기록된다.
    # 행동
    tracker.on_arrival(10.0)
    # 기대:
    assert tracker.last_time == 10.0


def test_arrival_time_is_replaced_by_next_message(tracker):
    # 요구: 새 메시지가 오면 기록이 새 시각으로 바뀐다.
    # 행동
    tracker.on_arrival(10.0)
    tracker.on_arrival(12.0)
    # 기대:
    assert tracker.age(12.0) == 0.0


def test_age_grows_while_no_message_arrives(tracker):
    # 요구: 메시지가 더 오지 않으면 기록은 그대로이고 경과만 늘어난다.
    # 행동
    tracker.on_arrival(10.0)
    # 기대: 기록, age(13.0), age(20.0)을 각각 확인한다
    assert tracker.age(13.0) == 3.0
    assert tracker.age(20.0) == 10.0
