"""
A module to evaluate datetimes and whether they are "on the edge"
of a German "Stromtag" or "Gastag" respectively
"""
from datetime import datetime
from enum import Enum
from typing import Callable

from bdew_datetimes.times import get_german_local_time


class Division(Enum):
    """
    Allows to distinguish divisions used by German utilities, German "Sparte".
    """

    STROM = 1  #: electricity
    GAS = 2  #: gas


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
    german_local_time = get_german_local_time(date_time)
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
    german_local_time = get_german_local_time(date_time)
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
