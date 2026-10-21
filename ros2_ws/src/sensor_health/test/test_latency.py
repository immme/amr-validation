import pytest

from sensor_health.latency import latency_sec

# 실수 계산에서 생기는 아주 작은 오차(약 3e-15초)는 허용하고 1나노초(1e-9초) 차이는
# 잡아내도록 abs=1e-12로 비교한다.


def test_latency_is_arrival_minus_stamp():
    """지연은 도착 시각에서 stamp 시각(sec에 nanosec을 초로 바꿔 더한 값)을 뺀 값이다."""
    assert latency_sec(100.30, 100, 100_000_000) == pytest.approx(0.2, abs=1e-12)


def test_latency_when_nanosec_is_zero():
    """nanosec이 0이면 stamp 시각은 sec 그대로다."""
    assert latency_sec(105.5, 100, 0) == pytest.approx(5.5, abs=1e-12)


def test_latency_when_nanosec_is_just_below_one_second():
    """nanosec이 1초 직전(999_999_999)이어도 sec에 더해 계산한다."""
    assert latency_sec(102.0, 100, 999_999_999) == pytest.approx(1.000_000_001, abs=1e-12)


def test_latency_is_negative_when_arrival_is_before_stamp():
    """도착이 stamp보다 앞서면 음수 지연을 그대로 돌려준다."""
    assert latency_sec(100.0, 100, 500_000_000) == pytest.approx(-0.5, abs=1e-12)
