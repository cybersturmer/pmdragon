from __future__ import annotations

from copy import deepcopy
from datetime import timedelta, date, datetime, time
from enum import Enum, auto
from typing import Dict, Union, Tuple, List, Optional

from analytics.time.range import DatetimeRange, DateRange
from analytics.time.slices import DatetimeSlices, TimeSlices

__author__ = 'Wladimir Stürmer'
__license__ = "GPL"
__version__ = '1.0.1'
__maintainer__ = 'Wladimir Stürmer'
__email__ = 'cybersturmer@ya.ru'


class Calendar:
    class ExceptionType(Enum):
        # Common exclusion can to be used in (planned)
        COMMON_EXCL = auto()

        # Common inclusion can to be used in (planned)
        COMMON_INCL = auto()

        # Unplanned
        PERSONAL_PLAN_EXCL = auto()
        PERSONAL_INCL = auto()

        PERSONAL_UNPLAN_EXCL = auto()

    def __init__(self,
                 range_: DateRange,
                 schedule: Dict[int, Dict[int, TimeSlices]],
                 calendar_map: Dict[int, DateRange],
                 common_exception_map: Dict[int, Tuple[DatetimeSlices, DatetimeSlices]]):

        assert type(range_) is DateRange, \
            f'Range argument should be DateRange type, got {type(range_)} instead'

        self._start = range_.start
        self._end = range_.end

        """
        Current cursor, using for 
        iteration __iter__ __next__
        """
        self._cursor = -1

        """
        This container we need for last data controlling
        """
        self._cursor_slices = DatetimeSlices()

        """
        Schedule
        Dict with calendars with dict of key for weekday and values of 
        DatetimeSlices of TimeRange {1: DatetimeSlices([TimeRange(time(hours=10),time(hours=12))])}
        """
        assert type(schedule) is dict, \
            'Schedule argument should be a dict with int keys and TimeSlices value'

        self._schedule = schedule

        """
        Calendar MAP
        Dict with key of active calendar for DatetimeRange 
        {1: DatetimeRange(
        datetime(year=2019, month=7, day=10, hours=10),
        datetime(year=2019, month=7, day=10, hours=12),
        )}
        
        Ranges have to be unique
        """
        assert type(calendar_map) is dict, \
            'Calendar MAP should be a dict with int keys and DateRange value'

        self.__calendar_map = calendar_map

        """
        Common exception MAP is dict of tuples {1: DatetimeSlices(DateTimeRange(from , to),
        DatetimeSlices(DatetimeRange(from, to)))}
        """
        assert type(common_exception_map) is dict, \
            'Common exception MAP should be a dict with' \
            ' int keys and tuple of (DatetimeSlices for inclusion,' \
            ' DatetimeSlices dor exclusion)'

        self.__common_exception_map = common_exception_map

        """
        Predefine exception dictionary as empty slices
        """
        self._exceptions = {num: DatetimeSlices() for num in self.ExceptionType}

    def cursor_schedule(self) -> Optional[Dict[int, TimeSlices]]:
        """
        Find schedule for current calendar_id and return None if calendar for cursor not found
        :return: dictionary with key of calendar_id and TimeSlices
                 for period of working
        """

        if self._cursor < 0:
            raise AttributeError('Cursor data accessible just over iteration,'
                                 ' example: for day in calendar:'
                                 'return calendar.cursor_slices()')

        """
        Founding  calendars with DatetimeRange
        including cursor date, should't return multiple calendars
        """
        cal_list = [cal_id
                    for cal_id, cal_range
                    in self.__calendar_map.items()
                    if cal_range.start <= self._start + timedelta(days=self._cursor) < cal_range.end]

        """
        If current cursor date not included by any given calendar DateRange,
        we return None, to say [No schedule] for cursor
        """
        if not cal_list:
            return None

        assert len(cal_list) == 1, \
            f'{len(cal_list)} calendars returned for date {self._start + timedelta(days=self._cursor)}'

        cal_id = cal_list.pop()

        try:
            schedule = self._schedule[cal_id]
        except KeyError:
            raise ValueError(f'Schedule data, given in arguments need information'
                             f' about calendar id:{cal_id} schedule, but Index Error instead')

        try:
            common_exceptions = self.__common_exception_map[cal_id]
        except IndexError:
            common_exceptions = DatetimeSlices(), DatetimeSlices()

        # @todo check
        self._exceptions[self.ExceptionType.COMMON_INCL], \
            self._exceptions[self.ExceptionType.COMMON_EXCL] = common_exceptions

        return schedule

    def cursor_common_slices(self) -> Union[DatetimeSlices, None]:
        schedule = self.cursor_schedule()

        """
        If we got None schedule or empty Schedule for day (for ex. weekend).
        We just return empty DatetimeSlices
        """
        if not schedule:
            return DatetimeSlices()

        weekday: int = (self._start + timedelta(days=self._cursor)).weekday()

        """
        For every range in week schedule create DatetimeRange, by
        combining date and time
        """

        li_slices = []

        if schedule[weekday]:
            for range_ in schedule[weekday]:
                _dt_start = datetime.combine(self._start + timedelta(days=self._cursor), range_.start)
                _dt_end = datetime.combine(self._start + timedelta(days=self._cursor), range_.end)

                _range = DatetimeRange(_dt_start, _dt_end)

                li_slices.append(_range)

        slices = DatetimeSlices(li_slices)

        """
        Exclude common exceptions (Checking for emptiness in TimeSlice)
        """
        if slices:
            slices.exclude(self._exceptions[self.ExceptionType.COMMON_EXCL])
            slices.exclude(self._exceptions[self.ExceptionType.PERSONAL_PLAN_EXCL])

        """
        Include common exceptions by adding just difference
        """
        if self.cursor_range in self.get_exceptions(self.ExceptionType.COMMON_INCL):
            slices.include_reversed_diff(self.get_exceptions(self.ExceptionType.COMMON_INCL))

        return slices

    def cursor_slices(self) -> DatetimeSlices:
        """
        :return: DatetimeSlices after adding/subtracting personal inclusion/exclusion
        """

        slices = self.cursor_common_slices()

        """
        If Common slices are empty, we still can add personal inclusion
        someone can have activity in non-active time
        """
        if not slices:
            """
            So now all common schedule is empty and we are ready to return
            an empty slice with inclusion that inside of this empty range
            """
            if self.cursor_range in self.get_exceptions(self.ExceptionType.PERSONAL_INCL):
                inclusion_exceptions = self.get_exceptions(self.ExceptionType.PERSONAL_INCL)
                inclusion_exceptions.crop_by_range(self.cursor_range)
                return inclusion_exceptions

            else:
                return DatetimeSlices()

        """
        With exclusion original DatetimeSlices cant to be empty
        """
        if slices and self.get_exceptions(self.ExceptionType.PERSONAL_PLAN_EXCL):
            personal_plan_exclusions = self.get_exceptions(self.ExceptionType.PERSONAL_PLAN_EXCL)
            slices.exclude(personal_plan_exclusions)

        if slices and self.get_exceptions(self.ExceptionType.PERSONAL_UNPLAN_EXCL):
            personal_unplan_exclusions = self.get_exceptions(self.ExceptionType.PERSONAL_UNPLAN_EXCL)
            slices.exclude(personal_unplan_exclusions)

        """
        Original DatetimeSlices can to be empty
        """
        if self.cursor_range in self.get_exceptions(self.ExceptionType.PERSONAL_INCL):
            personal_inclusions = self.get_exceptions(self.ExceptionType.PERSONAL_INCL)
            personal_inclusions.crop_by_range(self.cursor_range)
            slices.include(personal_inclusions)

        return slices

    @property
    def planned(self) -> DatetimeSlices:
        """
        :return: DatetimeSlices before adding/subtracting personal inclusion/exclusion
        """
        return self.cursor_common_slices()

    @property
    def actual(self) -> DatetimeSlices:
        """
        :return: DatetimeSlices after adding/subtracting personal inclusion/exclusion
        """
        return self.cursor_slices()

    @property
    def cursor(self) -> date:
        """
        :return: date for current cursor, by using start date and
        timedelta with cursor days
        """
        return self._start + timedelta(days=self._cursor)

    @property
    def cursor_next(self) -> date:
        """
        :return: date for current cursor, by using start date and
        timedelta with cursor days
        """
        return self._start + timedelta(days=self._cursor + 1)

    @property
    def cursor_range(self) -> DatetimeRange:
        """
        :return: DatetimeRange dor current cursor date
        from 00:00:00 of current day to 23:59:59 ... max of time()
        """
        cursor_from = datetime.combine(self.cursor, time.min)
        cursor_to = datetime.combine(self.cursor, time.max)

        return DatetimeRange(cursor_from, cursor_to)

    def __set_exception(self, exception_type: ExceptionType, exceptions: List[Tuple[datetime, datetime]]) -> Calendar:
        """
        :param exception_type: internal class for define ExceptionType
        :param exceptions: example [(2019-10-01 01:00:00, 2019-10-02 02:00:00),
         (2019-10-03 02:00:00, 2020-01-01 00:00:00)]
        :return: self
        """
        self._exceptions[exception_type].include(DatetimeSlices([DatetimeRange(exception[0], exception[1])
                                                                 for exception in exceptions]))
        return self

    def set_personal_planned_exclusions(self, exclusions: List[Tuple[datetime, datetime]]):
        """
        Set personal exclusion for calendar.
        Personal exclusion is independent from calendar_id
        """
        return self.__set_exception(self.ExceptionType.PERSONAL_PLAN_EXCL, exclusions)

    def set_personal_unplanned_exclusions(self, exclusions: List[Tuple[datetime, datetime]]):
        """
        Set personal exclusion for calendar.
        Personal exclusion is independent from calendar_id
        """
        return self.__set_exception(self.ExceptionType.PERSONAL_UNPLAN_EXCL, exclusions)

    def set_personal_inclusions(self, inclusions: List[Tuple[datetime, datetime]]):
        """
        Set personal inclusion for calendar
        Personal inclusion is independent from calendar_id
        Calendar use inclusions after exclusion, so if the same range was
        subtracted and added simultaneously - range will appear in final slices
        :param inclusions: [(2019-10-10 10:00:00, 2019-10-11 10:00:00)(2018-05-10 09:00:00, 2018-05-05 08:00:00)]
        :return:
        """
        return self.__set_exception(self.ExceptionType.PERSONAL_INCL, inclusions)

    """
    def set_common_exclusion
    def set_common_inclusion
    There is no method to set a common exception (inclusion/exclusion)
    Cuz common exception should be added through common_exception_map argument
    """
    def get_exceptions(self, exception_type: ExceptionType) -> DatetimeSlices:
        return deepcopy(self._exceptions[exception_type])

    def __next__(self) -> DatetimeSlices:
        """
        Using for iteration over days from start to end, by working schedule
        :return:
        """
        self._cursor += 1

        if self._start + timedelta(days=self._cursor) <= self._end:
            slices = self.cursor_slices()
            return slices

        else:
            raise StopIteration()

    def __iter__(self) -> Calendar:
        return self

    def __str__(self):
        cursor = self._start + timedelta(days=self._cursor)

        return f'{self._start} -> {cursor} wd:{cursor.weekday()} ->' \
            f' {self._end} com.excl.[{len(self._exceptions[self.ExceptionType.COMMON_EXCL])}]' \
            f' com.incl.[{len(self._exceptions[self.ExceptionType.COMMON_INCL])}]' \
            f' pers.excl.[{len(self._exceptions[self.ExceptionType.PERSONAL_PLAN_EXCL])}]' \
            f' pers.incl.[{len(self._exceptions[self.ExceptionType.PERSONAL_INCL])}]'

    __repr__ = __str__
