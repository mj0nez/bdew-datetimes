from datetime import date

import holidays
from holidays.constants import DEC
from holidays.countries.germany import Germany


class BdewHolidays(Germany):
    """Special holidays for the BDEW, excluding wide nation oder country specific holidays.

    To get a full calendar with all holidays use the function `create_bdew_calendar`.

    Currently, in Germany there are no observed holidays e.g. a Holiday is moved to the next Workday, if it's on Sunday.

    Nach GPKE und GeLi Gas sind alle jene Tage Werktage, die weder Sonnabend, Sonntag oder gesetzlicher Feiertag sind.
    Generell gelten der 24.12. und
    der 31.12. als Feiertage. Angaben ohne Gewähr.

    https://www.bdew.de/media/documents/GPKE-GeLiGas-Feiertagskalender-2022-Version-1-1_Uu1w6UQ.pdf

    [Accessed 2022-11-02]

    Parameters
    ----------
    Germany : _type_
        _description_
    """

    def __init__(self, observed: bool = False, **kwargs):
        kwargs.update({"observed": observed})
        super().__init__(**kwargs)

    def _populate(self, year):
        super()._populate(year)

        #
        self[date(year, DEC, 24)] = "Heiligabend"
        self[date(year, DEC, 31)] = "Silvester"


def create_bdew_calendar() -> holidays.HolidaySum:
    """Creates a calendar containing the holidays used by the BDEW.


    Returns
    -------
    holidays.HolidaySum
        dict-like holiday calendar, to check if a date/datetime is a holiday
    """

    # First we need the BDEW specific holidays.
    calendar = BdewHolidays()

    # If a day is holiday in any subdivision, the holiday is valid nationwide.
    # Therefore we add all subdivisions of Germany to the BDEW specific holidays.
    # Currently, in Germany holidays are not observed.
    for cal in calendar.subdivisions:
        calendar += Germany(subdiv=cal, observed=False)

    return calendar
