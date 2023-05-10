"""
A module to evaluate datetimes and whether they are "on the edge"
of a German "Stromtag" or "Gastag" respectively
"""
from datetime import datetime, time

# The problem with the stdlib zoneinfo is, that the availability of timezones
# via ZoneInfo(zone_key) depends on the OS and system on which you're running
# it. In some cases "Europe/Berlin" might be available, but generally it's not,
# and it's PITA to manually define timezones. So we're using pytz as a
# datasource for timezone information.
from pytz import utc

from bdew_datetimes import GERMAN_TIME_ZONE


def get_german_local_time(date_time: datetime) -> time:
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
