import pytest

from sensor_health.latency import latency_sec

# 실수 계산에서 생기는 아주 작은 오차(약 3e-15초)는 허용하고,
# 1나노초(1e-9초) 차이는 잡아내도록 abs=1e-12로 비교한다.


def test_latency_is_arrival_minus_stamp():
    # 요구: 지연은 도착 시각에서 stamp 시각을 뺀 값이다.
    #       stamp 시각은 sec에 nanosec을 초로 바꿔 더한 값이다.
    # 행동: 도착 100.30초, stamp는 sec 100, nanosec 100_000_000
    # 기대:
    assert latency_sec(100.30, 100, 100_000_000) == pytest.approx(0.2, abs=1e-12)


def test_latency_when_nanosec_is_zero():
    # 요구: nanosec이 0이면 stamp 시각은 sec 그대로다.
    # 행동: 도착 105.5초, stamp는 sec 100, nanosec 0
    # 기대:
    assert latency_sec(105.5, 100, 0) == pytest.approx(5.5, abs=1e-12)


def test_latency_when_nanosec_is_just_below_one_second():
    # 요구: nanosec이 1초 직전(999_999_999)이어도 sec에 더한 시각으로 계산한다.
    # 행동: 도착 102.0초, stamp는 sec 100, nanosec 999_999_999
    # 기대:
    assert latency_sec(102.0, 100, 999_999_999) == pytest.approx(1.000_000_001, abs=1e-12)


def test_latency_is_negative_when_arrival_is_before_stamp():
    # 요구: 도착 시각이 stamp보다 앞서면 음수 지연을 그대로 돌려준다.
    # 행동: 도착 100.0초, stamp는 sec 100, nanosec 500_000_000
    # 기대:
    assert latency_sec(100.0, 100, 500_000_000) == pytest.approx(-0.5, abs=1e-12)
