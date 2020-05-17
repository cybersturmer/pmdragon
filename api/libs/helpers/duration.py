from datetime import timedelta
from typing import List


def delta_to_hours(duration: timedelta) -> float:
    hours = duration.days * 24 + duration.seconds / 3600

    return round(hours, 1)


def total_seconds_list_to_delta(data: List[int]) -> timedelta:
    assert isinstance(data, list), 'Input data should be an list'
    return timedelta(seconds=sum(data))
