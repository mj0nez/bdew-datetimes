"""model classes used in this package"""

from dataclasses import dataclass
from typing import Literal, Union

from bdew_datetimes.enums import DayType, EndDateType

_DayTyp = Union[DayType, Literal["WT", "KT"]]


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


__all__ = ["Period"]
