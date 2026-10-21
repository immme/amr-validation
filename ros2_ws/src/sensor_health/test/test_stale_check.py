from sensor_health.stale_check import is_stale

# 실수(float)를 곱하면 경계값이 어긋날 수 있어, 밀리초 정수에 MS를 곱해 나노초로 바꾼다.
MS = 1_000_000  # 1밀리초 = 1,000,000나노초


def test_ok_well_before_timeout():
    """마지막 도착 뒤 timeout 전이면 OK다."""
    assert is_stale(11_000 * MS, 10_000 * MS, 2_000 * MS) is False


def test_ok_just_before_timeout():
    """timeout 1밀리초 전까지는 OK다."""
    assert is_stale(11_999 * MS, 10_000 * MS, 2_000 * MS) is False


def test_stale_at_exact_timeout():
    """경과 시간이 timeout과 같으면 STALE이다."""
    assert is_stale(12_000 * MS, 10_000 * MS, 2_000 * MS) is True


def test_stale_just_after_timeout():
    """timeout을 1밀리초 지나면 STALE이다."""
    assert is_stale(12_001 * MS, 10_000 * MS, 2_000 * MS) is True


def test_stale_before_first_message():
    """아직 한 번도 받지 못했으면 STALE이다."""
    assert is_stale(11_000 * MS, None, 2_000 * MS) is True
