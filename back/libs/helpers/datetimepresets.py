import calendar
from datetime import timedelta, date, datetime

import pytz
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now


def day_later():
    return timezone.now() + timedelta(hours=24)

# todo replace all functions to timezone aware datetime


def today():
    return datetime.combine(timezone.now().date(), datetime.min.time())


def date_after_year():
    today_ = today()

    return today_.replace(year=today_.year + 1)


def today_earliest():
    return datetime.combine(now().date(), datetime.min.time())


def today_latest():
    return datetime.combine(now().date(), datetime.max.time())


def one_year_later_midnight():
    _timestamp = now()
    return _timestamp.replace(hour=0, minute=0, second=0, microsecond=0, year=_timestamp.year + 1,
                              tzinfo=pytz.timezone(settings.TIME_ZONE))


def next_month(date_: date):
    month = date_.month
    year = date_.year + month // 12
    month = month % 12 + 1
    day = min(date_.day, calendar.monthrange(year, month)[1])
    return date(year=year, month=month, day=day)


def prev_month(date_: date):
    return date_.replace(day=1) - timedelta(days=1)


def month_extremum(year: int, month: int):
    min_date = date(year=year, month=month, day=1)
    max_date = min_date.replace(day=calendar.monthrange(year, month)[1])

    return min_date, max_date


def day_extremum(date_: date):
    return datetime.combine(date_, datetime.min.time()), \
           datetime.combine(date_, datetime.max.time())


def zero_delta():
    return timedelta(seconds=0)
