"""static timezone object for Berlin/Germany"""

from pytz import timezone

GERMAN_TIME_ZONE = timezone("Europe/Berlin")
__all__ = ["GERMAN_TIME_ZONE"]
