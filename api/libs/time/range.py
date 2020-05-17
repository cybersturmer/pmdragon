from __future__ import annotations

from datetime import datetime, date, time, timedelta
from enum import Enum, auto
from typing import Union

__author__ = 'Wladimir Stürmer'
__license__ = "GPL"
__version__ = '1.0.1'
__maintainer__ = 'Wladimir Stürmer'
__email__ = 'cybersturmer@ya.ru'


class TimeCrossType(Enum):
    """ Types of crossing between two Range """

    OUT_LEFT = auto()
    OUT_SIZE_LEFT = auto()
    TOUCH_LEFT = auto()
    IN_LEFT = auto()
    IN_LEFT_TOUCH = auto()
    IN_SIZE = auto()
    EQUAL = auto()
    IN_RIGHT_TOUCH = auto()
    IN_RIGHT = auto()
    TOUCH_RIGHT = auto()
    OUT_RIGHT = auto()
    OUT_SIZE_RIGHT = auto()
    OUT_SIZE = auto()


class BaseRange:
    IS_CROSSED = [TimeCrossType.EQUAL,
                  TimeCrossType.IN_LEFT,
                  TimeCrossType.IN_SIZE,
                  TimeCrossType.IN_LEFT_TOUCH,
                  TimeCrossType.IN_RIGHT_TOUCH,
                  TimeCrossType.IN_RIGHT,
                  TimeCrossType.OUT_SIZE,
                  TimeCrossType.OUT_SIZE_LEFT,
                  TimeCrossType.OUT_SIZE_RIGHT]

    TOUCH_OR_CROSSED = IS_CROSSED + [TimeCrossType.TOUCH_LEFT,
                                     TimeCrossType.TOUCH_RIGHT]

    ENLARGE_FROM_LEFT = [TimeCrossType.TOUCH_LEFT,
                         TimeCrossType.IN_LEFT]

    ENLARGE_FROM_RIGHT = [TimeCrossType.TOUCH_RIGHT,
                          TimeCrossType.IN_RIGHT]

    INSIDE = [TimeCrossType.EQUAL,
              TimeCrossType.IN_SIZE,
              TimeCrossType.IN_LEFT_TOUCH,
              TimeCrossType.IN_RIGHT_TOUCH]

    NOT_CROSSED = [TimeCrossType.OUT_LEFT,
                   TimeCrossType.TOUCH_LEFT,
                   TimeCrossType.TOUCH_RIGHT,
                   TimeCrossType.OUT_RIGHT]

    NOT_TOUCH = [TimeCrossType.OUT_RIGHT, TimeCrossType.OUT_LEFT]

    OUT_SIZE_LEFT_OR_RIGHT = [TimeCrossType.OUT_SIZE,
                              TimeCrossType.OUT_SIZE_LEFT,
                              TimeCrossType.OUT_SIZE_RIGHT]

    def __init__(self,
                 _from: Union[datetime, date, time] = None,
                 _to: Union[datetime, date, time] = None):

        assert isinstance(_from, datetime) or \
               isinstance(_from, date) or \
               isinstance(_from, time), \
            f'From: {_from} should be datetime or date or time, but {type(_from)} instead'

        assert type(_from) == type(_to), \
            f'Both of ({_from}|{_to}) should be equal types, but ({type(_from)}|{type(_to)}) instead'

        assert _to > _from, f'{_to} should be more than {_from}'

        self._from = _from
        self._to = _to

    def __add__(self, other: __class__) -> tuple:
        """ Get same sub instance and return tuple
        As a result can return tuple of base range sub instances
        """

        assert isinstance(other, self.__class__), \
            f'Adding data should be the same type ({self.__class__}), got {type(other)} instead'

        _cross_type = self.cross_type(other)

        if _cross_type in self.ENLARGE_FROM_LEFT:
            return self.__class__(other.start, self.end),

        elif _cross_type in self.INSIDE:
            return self,

        elif _cross_type in self.ENLARGE_FROM_RIGHT:
            return self.__class__(self.start, other.end),

        elif _cross_type in self.NOT_TOUCH:

            return self, other

        elif _cross_type in self.OUT_SIZE_LEFT_OR_RIGHT:
            return other,

        else:
            raise ValueError(f'Unexpected cross type found: {_cross_type}')

    def __iadd__(self, other):
        """ Get another range and return tuple
         of ranges equally to normal"""

        return self + other

    def __sub__(self, other: __class__):
        """ Get another range and return tuple
        of ranges """

        assert isinstance(other, self.__class__), \
            f'Subtracting data should be the same type ({self.__class__}), got {type(other)} instead'

        _cross_type = self.cross_type(other)

        if _cross_type in self.NOT_CROSSED:
            return self,

        elif _cross_type in self.OUT_SIZE_LEFT_OR_RIGHT + [TimeCrossType.EQUAL]:
            return ()

        elif _cross_type in [TimeCrossType.IN_LEFT,
                             TimeCrossType.IN_LEFT_TOUCH]:

            return self.__class__(other.end, self.end),

        elif _cross_type is TimeCrossType.IN_SIZE:
            return self.__class__(self.start, other.start), self.__class__(other.end, self.end)

        elif _cross_type in [TimeCrossType.IN_RIGHT,
                             TimeCrossType.IN_RIGHT_TOUCH]:

            return self.__class__(self.start, other.start),

        else:
            raise ValueError(f'Unexpected cross type found: {_cross_type}')

    def __isub__(self, other):
        return self - other

    def __eq__(self, other) -> bool:
        """ Two range can to be equal just
        when start and end are totally equals """

        return self.cross_type(other) is TimeCrossType.EQUAL

    @property
    def start(self) -> Union[datetime, time, date]:
        return self._from

    @property
    def end(self) -> Union[datetime, time, date]:
        return self._to

    def cross_type(self, other: __class__) -> TimeCrossType:
        """ Get crossing type between two BaseRange instances self and other
            We can decide it by comparison of start and end between ranges """

        assert isinstance(other, self.__class__), \
            f'Adding data should be the same type ({self.__class__}), got {type(other)} instead'

        if other.end < self.start:
            return TimeCrossType.OUT_LEFT

        elif other.start < self.start < self.end == other.end:
            return TimeCrossType.OUT_SIZE_LEFT

        elif other.end == self.start:
            return TimeCrossType.TOUCH_LEFT

        elif other.start < self.start < other.end < self.end:
            return TimeCrossType.IN_LEFT

        elif other.start == self.start < other.end == self.end:
            return TimeCrossType.EQUAL

        elif self.start < other.start < other.end < self.end:
            return TimeCrossType.IN_SIZE

        elif self.start == other.start and other.end < self.end:
            return TimeCrossType.IN_LEFT_TOUCH

        elif self.start < other.start and self.end == other.end:
            return TimeCrossType.IN_RIGHT_TOUCH

        elif self.start < other.start < self.end < other.end:
            return TimeCrossType.IN_RIGHT

        elif other.start == self.end:
            return TimeCrossType.TOUCH_RIGHT

        elif self.start == other.start < self.end < other.end:
            return TimeCrossType.OUT_SIZE_RIGHT

        elif self.end < other.start:
            return TimeCrossType.OUT_RIGHT

        elif other.start < self.start < self.end < other.end:
            return TimeCrossType.OUT_SIZE

        else:
            raise ValueError(self, other, 'Unexpected behaving of comparison')

    def is_crossed(self, other: __class__) -> bool:
        _cross_type = self.cross_type(other)

        return _cross_type in self.IS_CROSSED

    def is_touched_or_crossed(self, other: __class__) -> bool:
        _cross_type = self.cross_type(other)

        return _cross_type in self.TOUCH_OR_CROSSED

    def __contains__(self, other: Union[date, datetime, BaseRange]):
        if issubclass(type(other), BaseRange):
            return self.is_crossed(other)

        elif isinstance(other, date):
            if self.__class__ == DateRange:
                return NotImplemented

            elif self.__class__ == DatetimeRange:
                from_datetime = datetime.combine(other, datetime.min.time())
                to_datetime = from_datetime + timedelta(days=1)
                comparable_object = DatetimeRange(from_datetime, to_datetime)

                return self.is_crossed(comparable_object)

        else:
            return NotImplemented

    def __str__(self):
        return f'{self.__class__.__name__}<{self.start}-{self.end}>'

    __repr__ = __str__


class DateRange(BaseRange):
    def to_datetime_range(self, time_range: TimeRange):
        c_date = self.start
        time_slices_list = []

        while c_date <= self.end:
            time_slices_list.append(
                DatetimeRange(datetime.combine(c_date, time_range.start),
                              datetime.combine(c_date, time_range.end)))

            c_date += timedelta(days=1)

        return tuple(time_slices_list)

    @property
    def days(self) -> int:
        return (self.end - self.start).days


class TimeRange(BaseRange):
    pass


class DatetimeRange(BaseRange):
    def __init__(self, start: datetime, end: datetime):
        assert isinstance(start, datetime), \
            f'From: {start} should be datetime, but {type(start)} instead'

        assert type(start) == type(end), \
            f'Both of ({start}|{end}) should be equal types, but ({type(start)}|{type(end)}) instead'

        super().__init__(start, end)

    @property
    def duration(self) -> timedelta:
        self._to: datetime
        self._from: datetime

        return self._to - self._from

    @property
    def total_seconds(self) -> int:
        return int(self.duration.total_seconds())

    def __str__(self):
        if self.start.date() == self.end.date():
            return f'{self.__class__.__name__}<{self.start.date()} {self.start.time()}-{self.end.time()}>'
        else:
            return super().__str__()
