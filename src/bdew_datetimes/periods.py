"""
periods is a module that helps to calculate statutory periods
("gesetzliche Fristen") in the German energy market.
It is based on the chapter "Fristenberechnung" in the GPKE.
"""

import datetime
from datetime import date
from typing import Optional

from dateutil.relativedelta import relativedelta
from holidays import SAT, SUN  # type:ignore[attr-defined]

from bdew_datetimes.calendar import create_bdew_calendar
from bdew_datetimes.enums import DayType, EndDateType, MonthType
from bdew_datetimes.models import Period
from bdew_datetimes.german_time_zone import GERMAN_TIME_ZONE

# https://www.bundesnetzagentur.de/DE/Beschlusskammern/1_GZ/BK6-GZ/2020/BK6-20-160/Mitteilung_Nr_2/Leseversion_GPKE.pdf
# pages 15 onwards

_bdew_calendar = create_bdew_calendar()
"""
a static calendar object that is used (module) internally
"""


def is_bdew_working_day(candidate: date) -> bool:
    """
    Returns true if and only if the given candidate is a day relevant for the period calculation.
    Returns false if the given candidate is either a BDEW holiday, a saturday or sunday.
    """
    if candidate in _bdew_calendar:
        return False
    return candidate.weekday() not in (SAT, SUN)


def get_next_working_day(start_date: date) -> date:
    """
    If start_date is a working day, the next (+1) working day is returned.
    If this day is a BDEW holiday or falls on a weekend, the next working day
    is returned.
    """
    result = start_date + datetime.timedelta(
        days=1
    )  # in any case the calculation starts at least at the next day
    while not is_bdew_working_day(result):
        # if the next day is a holiday, then we add days until we find a working day
        result += datetime.timedelta(days=1)
    return result


def get_previous_working_day(start_date: date) -> date:
    """
    If start_date is a working day, the previous (-1) working day is returned.
    If this day is a BDEW holiday or falls on a weekend, the previous working day
    is returned.
    """
    result = start_date - datetime.timedelta(
        days=1
    )  # in any case the calculation starts at least at the next day
    while not is_bdew_working_day(result):
        # if the previous day is a holiday, then we subtract days until we find a working day
        result -= datetime.timedelta(days=1)
    return result


def add_frist(start: date, period: Period) -> date:
    """
    Returns the date that is period after start.
    """
    result: date = start
    if period.number_of_days >= 0:
        # the period calculation starts at the next working day, even if the number_of_days == 0
        result = get_next_working_day(result)
    # result is now the "Beginndatum" of the Fristenberechnung
    if period.day_type == DayType.CALENDAR_DAY:
        return result + datetime.timedelta(days=period.number_of_days)
    # day_type is working day
    if period.number_of_days == 0:
        return result
    if period.number_of_days > 0:
        days_added = 0
        while days_added < period.number_of_days:
            result += datetime.timedelta(days=1)
            if is_bdew_working_day(result):
                # it's a usual working day; those are considered for the period calculation
                days_added += 1
    else:  # implicitly: elif period.number_of_days < 0:
        days_subtracted = 0
        while days_subtracted <= abs(period.number_of_days):
            result -= datetime.timedelta(days=1)
            if is_bdew_working_day(result):
                days_subtracted += 1
    return result


def get_nth_working_day_of_month(
    number_of_working_day_in_month: int,
    month_type: MonthType = MonthType.LIEFERMONAT,
    start: Optional[date] = None,
) -> date:
    """
    Returns the nth working of the month, starting at start.
    If start is None, then we use the local date/start of month in Germany.
    Only year and month of the provided start date are taken into account.
    The date.day is always discarded.

    This function is useful if you're dealing with statutory periods from the
    GPKE/MaBiS that are defined as "working days since start of month".
    """
    if start is None:
        start = GERMAN_TIME_ZONE.localize(datetime.datetime.utcnow()).date()
    if month_type == MonthType.LIEFERMONAT:
        # returns the "nter Werktag des Liefermonats"
        start = get_previous_working_day(start.replace(day=1))
        period = Period(
            number_of_days=number_of_working_day_in_month,
            day_type=DayType.WORKING_DAY,
            end_date_type=EndDateType.INCLUSIVE,
        )
        result = add_frist(start, period)
    elif month_type == MonthType.FRISTENMONAT:
        # returns the "nter Werktag des Fristenmonats"
        start_of_next_month = start.replace(day=1) + relativedelta(months=1)
        result = get_nth_working_day_of_month(
            number_of_working_day_in_month,
            month_type=MonthType.LIEFERMONAT,
            start=start_of_next_month,
        )
    else:
        raise ValueError(f"Unhandled month_type {month_type}")
    return result


# pylint:disable=duplicate-code
__all__ = [
    "is_bdew_working_day",
    "get_next_working_day",
    "get_previous_working_day",
    "add_frist",
    "get_nth_working_day_of_month",
]
