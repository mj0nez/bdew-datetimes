"""
contains the business logic (namely the BDEW calendar information)

"""
from datetime import date

from holidays import HolidayBase, HolidaySum
from holidays.constants import DEC
from holidays.countries.germany import Germany


class BdewDefinedHolidays(HolidayBase):
    """
    Special holidays considered by the BDEW, excluding nationwide or state specific holidays.

    To get a full calendar with all holidays use the function `create_bdew_calendar`.

    Currently, in Germany there are no observed holidays e.g. a Holiday is
    moved to the next Workday, if it's on Sunday.

    """

    def __init__(self, observed: bool = False, **kwargs):
        super().__init__(observed=observed, **kwargs)

    def _populate(self, year):
        self[date(year, DEC, 24)] = "Heiligabend"
        self[date(year, DEC, 31)] = "Silvester"


def create_bdew_calendar() -> HolidaySum:
    """Creates a calendar containing all days considered by the BDEW.

    Currently, in Germany there are no observed holidays e.g. a Holiday is
    moved to the next Workday, if it's on Sunday.

    "Nach GPKE und GeLi Gas sind alle jene Tage Werktage, die weder Sonnabend,
    Sonntag oder gesetzlicher Feiertag sind. Generell gelten der 24.12. und
    der 31.12. als Feiertage. Angaben ohne Gewähr."

    https://www.bdew.de/media/documents/GPKE-GeLiGas-Feiertagskalender-2022-Version-1-1_Uu1w6UQ.pdf

    [Accessed 2022-11-02]``

    Returns
    -------
    holidays.HolidaySum
        dict-like holiday calendar, to check if a date/datetime is a holiday
    """

    # First we need the BDEW specific holidays.
    calendar = BdewDefinedHolidays()

    # the type is wrong at assignment but correct after the first loop interation
    result: HolidaySum = calendar  # type:ignore[assignment]

    # If a day is holiday in any subdivision, the holiday is valid nationwide.
    # Therefore, we add all subdivisions of Germany to the BDEW specific holidays.
    # Currently, in Germany holidays are not observed.
    for subdivision in Germany.subdivisions:
        # the method __add__ expects a Union[int, "HolidayBase", "HolidaySum"] as `other`
        # here, we're dealing with a child instance of HolidayBase
        result += Germany(
            subdiv=subdivision, observed=False
        )  # type:ignore[assignment]

    return result
