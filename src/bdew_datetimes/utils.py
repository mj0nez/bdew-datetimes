"""
helper functions
"""

from datetime import date, timedelta

from bdew_datetimes.calendar import create_bdew_calendar

_bdew_calendar = create_bdew_calendar()


def _get_all(is_working_day: bool, year: int) -> list[date]:
    """
    Returns a list of all BDEW working days or non-working days in the given year.
    """
    days = []
    current_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    while current_date <= end_date:
        if _bdew_calendar.is_working_day(current_date) == is_working_day:
            days.append(current_date)
        current_date += timedelta(days=1)

    return days


def get_all_bdew_working_days(year: int) -> list[date]:
    """
    Returns a list of all BDEW working days in the given year.
    This includes all weekdays except saturday and sunday that are not BDEW holidays.
    """
    return _get_all(is_working_day=True, year=year)


def get_all_bdew_non_working_days(
    year: int, include_weekends: bool
) -> list[date]:
    """
    Returns a list of all BDEW working days in the given year.
    """
    non_working_days = _get_all(is_working_day=False, year=year)
    if include_weekends:
        return non_working_days
    return [d for d in non_working_days if d.weekday() not in (5, 6)]


__all__ = ["get_all_bdew_working_days", "get_all_bdew_non_working_days"]
