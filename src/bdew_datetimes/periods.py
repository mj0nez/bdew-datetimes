"""
periods is a module that helps to calculate statutory periods
("gesetzliche Fristen") in the German energy market.
It is based on the chapter "Fristenberechnung" in the GPKE.
"""
import datetime
import sys
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional, Union

from dateutil.relativedelta import relativedelta
from holidays import SAT, SUN

from bdew_datetimes import GERMAN_TIME_ZONE, create_bdew_calendar

try:
    from typing import Literal
except ImportError:  # for Python 3.7
    pass

# https://www.bundesnetzagentur.de/DE/Beschlusskammern/1_GZ/BK6-GZ/2020/BK6-20-160/Mitteilung_Nr_2/Leseversion_GPKE.pdf
# pages 15 onwards

_bdew_calendar = create_bdew_calendar()
"""
a static calendar object that is used (module) internally
"""


class DayType(str, Enum):
    """
    An enum to differentiate between calendar days and working days.
    """

    WORKING_DAY = "WT"  #: working day, German "Werktag"
    CALENDAR_DAY = "KT"  #: calendar day, German "Kalendertag"


class EndDateType(Enum):
    """
    An enum to distinguish inclusive and exclusive end dates.
    """

    INCLUSIVE = 1
    """
    If a contract ends with the year 2022 and the end date is denoted as "2022-12-31",
    then the end date is inclusive. Most dates in human (spoken) communication are meant
    inclusively.
    """

    EXCLUSIVE = 2
    """
    If a constract ends with the year 2022 and the end date is denoted as "2023-01-01",
    then the end date is exclusive. Most end dates handled by technical systems are meant
    exclusively.
    """


if sys.version_info.minor > 7:
    _DayTyp = Union[DayType, Literal["WT", "KT"]]
else:
    _DayTyp = Union[DayType, str]  # type:ignore[misc]


@dataclass
class Period:
    """
    A period is a German "Frist": A tuple that consists of a number of days and a day type.
    """

    number_of_days: int
    """
    number of days (might be any value <0, >0 or ==0)
    """
    day_type: DayType
    """
    the kind of days to add/subtract
    """

    def __init__(
        self,
        number_of_days: int,
        day_type: _DayTyp,
        end_date_type: EndDateType = EndDateType.EXCLUSIVE,
    ):
        """
        Initialize the Period by providing a number of days and a day_type which define the period.

        """
        self.number_of_days = number_of_days
        # If the Period is about something ending (e.g. a contract), then the user may
        # provide an end_date_type.
        # Internally we handle all end dates as exclusive, because:
        # https://hf-kklein.github.io/exclusive_end_dates.github.io/
        if end_date_type == EndDateType.INCLUSIVE:
            if self.number_of_days > 0:
                self.number_of_days = self.number_of_days - 1
            elif self.number_of_days < 0:
                self.number_of_days = self.number_of_days + 1
        if isinstance(day_type, DayType):
            pass
        elif isinstance(day_type, str):
            day_type = DayType(day_type)
        else:
            raise ValueError(
                f"'{day_type}' is not an allowed value; Check the typing"
            )
        self.day_type: DayType = day_type


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


class MonthType(Enum):
    """
    When calculating periods defined as 'nth working day of a month' the
    BNetzA regulations distinguish between two types of month which are
    modelled in this enum.
    Some periods refer to the "Liefermonat", others to the "Fristenmonat".
    """

    LIEFERMONAT = 1
    """
    The "Liefermonat" is the month in which the supply starts.
    """
    FRISTENMONAT = 2
    """
    The grid operators prefer a key date based handling of supply contracts.
    The key date in these cases is usually expressed as a specific working day
    in the so called "Fristenmonat".
    The "Fristenmonat" starts at the first day of the month
    _before_ the "Liefermonat".
    Quote: 'Nach der Festlegung BK6-06-009 (GPKE) der Monat vor dem Liefermonat.'
    """
    # pylint:disable=line-too-long
    # source: https://www.bundesnetzagentur.de/DE/Beschlusskammern/1_GZ/BK6-GZ/_bis_2010/2006/BK6-06-009/BK6-06-009_Beschluss_download.pdf?__blob=publicationFile&v=5


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
