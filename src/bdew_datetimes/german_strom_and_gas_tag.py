"""
A module to evaluate datetimes and whether they are "on the edge"
of a German "Stromtag" or "Gastag" respectively
"""
from datetime import datetime, time
from enum import Enum
from typing import Callable

# The problem with the stdlib zoneinfo is, that the availability of timezones
# via ZoneInfo(zone_key) depends on the OS and system on which you're running
# it. In some cases "Europe/Berlin" might be available, but generally it's not,
# and it's PITA to manually define timezones. So we're using pytz as a
# datasource for timezone information.
from pytz import utc

from bdew_datetimes import GERMAN_TIME_ZONE


class Division(Enum):
    """
    Allows to distinguish divisions used by German utilities, German "Sparte".
    """

    STROM = 1  #: electricity
    GAS = 2  #: gas


def _get_german_local_time(date_time: datetime) -> time:
    """
    Returns the current german local time for the given datetime object.
    """
    german_local_datetime = date_time.astimezone(GERMAN_TIME_ZONE)
    return german_local_datetime.time()


def has_no_utc_offset(date_time: datetime) -> bool:
    """
    Returns true if and only if date_time has an explicit offset to UTC.
    If the UTC-offset is 0, it is exactly "+00:00".
    """
    # the name of the function contains a negation because in German
    # market communication it often matters that the UTC offset is 0.
    original_time = date_time.time()
    utc_time = date_time.astimezone(tz=utc).time()
    return (
        utc_time == original_time
        and utc_time.hour == 0
        and utc_time.minute == 0
        and utc_time.second == 0
    )


def is_stromtag_limit(
    date_time: datetime,
) -> bool:  # the name is not as speaking as I'd like it to be
    """
    Returns true if and only if the given date_time is the inclusive
    start or exclusive end of a german "Stromtag".
    The "Stromtag" is the balancing relevant day in the German electricity
    market.
    It starts and ends at midnight in German local time which can be
    either 23:00 h or 22:00 h in UTC (depending on the daylight saving time in Germany).
    """
    german_local_time = _get_german_local_time(date_time)
    return (
        german_local_time.hour == 0
        and german_local_time.minute == 0
        and german_local_time.second == 0
    )


def is_gastag_limit(
    date_time: datetime,
) -> bool:  # the name is not as speaking as I'd like it to be
    """
    Returns true if and only if the given date_time is the inclusive start
    or exclusive end of a german "Gastag".
    The "Gastag" is the balancing relevant day in the German gas market.
    It starts and ends at 6am in German local time which can be either
    04:00 h or 05:00 h in UTC (depending on the daylight saving time in Germany).
    """
    german_local_time = _get_german_local_time(date_time)
    return (
        german_local_time.hour == 6
        and german_local_time.minute == 0
        and german_local_time.second == 0
    )


def is_xtag_limit(date_time: datetime, division: Division) -> bool:
    """
    Evaluates if it is the start/end of a provided division.
    """
    xtag_evaluator: Callable[[datetime], bool]
    if division == Division.STROM:
        xtag_evaluator = is_stromtag_limit
    elif division == Division.GAS:
        xtag_evaluator = is_gastag_limit
    else:
        raise NotImplementedError(
            f"The division must either be 'Strom' or 'Gas': '{division}'"
        )
    return xtag_evaluator(date_time)
