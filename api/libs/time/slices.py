#!/usr/bin/env python
""" Provides TimeSlices class for dealing with DatetimeRange lists """

from __future__ import annotations

from copy import deepcopy
from datetime import timedelta
from operator import attrgetter
from typing import List, Union, Tuple, NoReturn, Optional

from analytics.time.range import BaseRange, DatetimeRange

__author__ = 'Wladimir Stürmer'
__license__ = "GPL"
__version__ = '1.0.1'
__maintainer__ = 'Wladimir Stürmer'
__email__ = 'cybersturmer@ya.ru'


class BaseSlices:
    def __init__(self, list_: Union[List[BaseRange], Tuple[BaseRange, ...]] = ()):

        assert isinstance(list_, tuple) or isinstance(list_, list), \
            f'Argument should be tuple or list, got {type(list_)} instead'

        self._iter_index = 0
        self._slices = []

        self._content_type = None

        if len(list_) > 0:
            self._content_type = list_[0].__class__

            for el in list_:
                assert self._content_type == el.__class__,\
                    f'Incompatible {self._content_type} and {el.__class__} elements in same slice'

                self._include_range(el)

    @property
    def slices(self) -> List:
        return self._slices

    @property
    def is_empty(self):
        return len(self._slices) == 0

    def _get_crossed_indexes(self, other: BaseRange) -> List[int]:
        """ Get indexes in current TimeSlice that crossed with given BaseRange """

        assert issubclass(type(other), BaseRange), \
            f'Just BaseRange subclasses are accepted,  got {other.__class__.__name__} instead'

        return [_index for _index, _slice in reversed(list(enumerate(self._slices))) if other in _slice]

    def _get_touched_or_crossed(self, other: BaseRange) -> List[int]:
        """ Get indexes for all (BaseRange) in TimeSlice, that cross
            or touches with given (BaseRange) """

        assert issubclass(type(other), BaseRange), \
            f'Just BaseRange subclasses are accepted, got {other.__class__.__name__} instead'

        return [_index
                for _index, _slice in reversed(list(enumerate(self._slices)))
                if other.is_touched_or_crossed(_slice)]

    def _remove_slices_by_indexes(self, indexes: List[int]) -> NoReturn:
        """ Remove slices in current TimeSlice be indexes list """

        for _index in indexes:
            del self._slices[_index]

    def _sort_slices(self) -> NoReturn:
        """ Sort all slices by start value """

        def _sort_start(item):
            return item.start

        self._slices.sort(key=_sort_start)

    def _include_range(self, other: BaseRange) -> BaseSlices:
        """ Include BaseRange subclass to TimeSlice """

        if self.is_empty:
            self._slices = [other]
            return self

        cross_indexes_list = self._get_touched_or_crossed(other)

        if not cross_indexes_list:
            self._slices.append(other)
            self._sort_slices()
            return self

        else:
            cross_values_list = [self._slices[_index] for _index in cross_indexes_list]
            cross_values_list.append(other)

            self._remove_slices_by_indexes(cross_indexes_list)

            _min, _max = min(cross_values_list, key=attrgetter('start')), \
                         max(cross_values_list, key=attrgetter('end'))

            mod_base_range = other.__class__(_min.start, _max.end)
            self._slices.append(mod_base_range)
            self._sort_slices()

            return self

    def get_diff(self, other):
        return self - other

    def get_reversed_diff(self, other):
        return other - self

    def include(self, other: Union[BaseRange, BaseSlices]) -> BaseSlices:
        """ Include BaseRange or TimeSlices to current TimeSlice
            return TimeSlice after computing """

        is_base_range_sub = issubclass(type(other), BaseRange)
        is_time_slice = isinstance(other, self.__class__)

        assert is_base_range_sub or is_time_slice, \
            f'Just BaseRange subclasses and {self.__class__.__name__} accepted, got {type(other)} instead'

        if is_base_range_sub:
            return self._include_range(other)

        elif is_time_slice:
            if not self:
                self._slices = other.slices
                return self

            if not other:
                return self

            for other_base_range in other:
                self._include_range(other_base_range)

            return self

    def include_reversed_diff(self, other: BaseSlices):
        if other:
            diff = self.get_reversed_diff(other)
            self.include(diff)

        return self

    def _exclude_range(self, other: BaseRange) -> BaseSlices:
        """ Exclude BaseRange subclasses from current TimeSlice and
            return TimeSlice after computing """

        cross_indexes_list = self._get_crossed_indexes(other)

        if not cross_indexes_list:
            return self

        cross_value_list = [self.slices[_index] for _index in cross_indexes_list]
        mod_time_slices_list = []

        for cross_value in cross_value_list:
            sub_time_slice = cross_value - other

            for _base_range in sub_time_slice:
                mod_time_slices_list.append(_base_range)

        self._remove_slices_by_indexes(cross_indexes_list)

        for _base_range in mod_time_slices_list:
            self._slices.append(_base_range)

        self._sort_slices()

        return self

    def exclude(self, other: Union[BaseRange, BaseSlices]) -> BaseSlices:
        """ Exclude BaseRange or TimeSlice from current TimeSlice and
            TimeSlice after computing """

        is_base_range_sub = issubclass(type(other), BaseRange)
        is_time_slice = isinstance(other, self.__class__)

        assert is_base_range_sub or is_time_slice, \
            f'Just BaseRange subclasses and {self.__class__} accepted, got {type(other)} instead'

        if is_base_range_sub:
            self._exclude_range(other)
            return self

        elif is_time_slice:
            if not other:
                return self

            for _base_range in other:
                if _base_range.end < other.first.start or _base_range.start > other.last.end:
                    continue

                self.exclude(_base_range)

            return self

    def exclude_diff(self, other: BaseSlices):
        diff = self.get_diff(other)
        self.exclude(diff)

        return self

    @property
    def first(self) -> Optional[BaseRange]:
        if self.is_empty:
            return None

        return self._slices[0]

    @property
    def last(self) -> Optional[BaseRange]:
        if self.is_empty:
            return None

        return self._slices[-1]

    def __bool__(self):
        return not self.is_empty

    def __add__(self, other: Union[BaseRange, BaseSlices]) -> BaseSlices:
        self.include(other)

        return self

    def __iadd__(self, other: Union[BaseRange, BaseSlices]) -> BaseSlices:
        self.include(other)

        return self

    def __sub__(self, other: Union[BaseRange, BaseSlices]) -> BaseSlices:
        self.exclude(other)

        return self

    def __isub__(self, other: Union[BaseRange, BaseSlices]) -> BaseSlices:
        return self - other

    def __getitem__(self, index: int) -> BaseRange:
        return self._slices[index]

    def __len__(self) -> int:
        return len(self._slices)

    def __iter__(self) -> BaseSlices:
        self._iter_index = 0
        return self

    def __next__(self) -> BaseRange:
        try:
            item = self._slices[self._iter_index]

        except IndexError:
            self._iter_index = 0
            raise StopIteration

        else:
            self._iter_index += 1
            return item

    def __eq__(self, other) -> bool:
        assert isinstance(other, BaseSlices), \
            'comparable object should be TimeSlice\'s instance'

        if len(self.slices) != len(other.slices):
            return False

        for _original_slice, _other_slice in zip(self._slices, other._slices):
            if _original_slice != _other_slice:
                return False

        return True

    def __str__(self) -> str:
        snippet = []

        for _slice in self._slices:
            snippet.append(str(_slice))

        return f'{self.__class__.__name__}:' + ','.join(snippet)

    def __repr__(self) -> str:
        return self.__str__()

    def __contains__(self, other):
        # @todo check type of other
        for _range in self.slices:
            if other in _range:
                return True

        return False


class DatetimeSlices(BaseSlices):
    def __init__(self, list_: Union[List[DatetimeRange], Tuple[DatetimeRange, ...]] = ()):
        super(DatetimeSlices, self).__init__(list_)

        assert isinstance(list_, tuple) or isinstance(list_, list), \
            f'Argument should be tuple or list, got {type(list_)} instead'

    def crop_by_range(self, datetime_range: DatetimeRange):
        return self - (deepcopy(self) - DatetimeSlices([datetime_range]))

    @property
    def duration(self):
        if self.is_empty:
            return timedelta(seconds=0)

        total_seconds = sum([slice_.duration.total_seconds() for slice_ in self._slices])

        return timedelta(seconds=total_seconds)


class TimeSlices(BaseSlices):
    pass
