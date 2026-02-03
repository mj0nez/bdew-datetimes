"""
contains the business logic (namely the BDEW calendar information)

"""

from datetime import date
from typing import Any

from holidays import HolidayBase, HolidaySum
from holidays.constants import DEC, JUN  # type: ignore[attr-defined]
from holidays.countries.germany import Germany


class BdewDefinedHolidays(HolidayBase):
    """
    Special holidays considered by the BDEW, excluding nationwide or state specific holidays.

    To get a full calendar with all holidays use the function `create_bdew_calendar`.

    Currently, in Germany there are no observed holidays e.g. a Holiday is
    moved to the next Workday, if it's on Sunday.

    """

    def __init__(self, observed: bool = False, **kwargs: Any) -> None:
        super().__init__(observed=observed, **kwargs)

    def _populate(self, year: int) -> None:
        self[date(year, DEC, 24)] = "Heiligabend"
        self[date(year, DEC, 31)] = "Silvester"
        if year == 2025:
            self[date(2025, JUN, 6)] = (
                "Sonderfeiertag"
                # Anlässlich der (verschobenen) Einführung des 24h Lieferantenwechsels
            )


_relevant_subdivisions: list[str] = [
    "BB",  # Brandenburg.
    "BE",  # Berlin.
    "BW",  # Baden-Württemberg.
    "BY",  # Bayern.
    "HB",  # Bremen.
    "HE",  # Hessen.
    "HH",  # Hamburg.
    "MV",  # Mecklenburg-Vorpommern.
    "NI",  # Niedersachsen.
    "NW",  # Nordrhein-Westfalen.
    "RP",  # Rheinland-Pfalz.
    "SH",  # Schleswig-Holstein.
    "SL",  # Saarland.
    "SN",  # Sachsen.
    "ST",  # Sachsen-Anhalt.
    "TH",  # Thüringen.
    # This list contains an explicit list of all BDEW calendar relevant Germany subdivisions.
    # It does _not_ include the 'Augsburg' subdivision which has been added in holidays v0.78.
    # https://github.com/vacanza/holidays/commit/feab68b4377369ad52eeee9e98fc8316ec0c6f86
]


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
    calendar = BdewDefinedHolidays(language="de")

    # the type is wrong at assignment but correct after the first loop iteration
    result: HolidaySum = calendar  # type: ignore[assignment]
    original_language_before_adding_subdivisions = result.language
    # If a day is holiday in any subdivision, the holiday is valid nationwide.
    # Therefore, we add all subdivisions of Germany to the BDEW specific holidays.
    # Currently, in Germany holidays are not observed.
    for subdivision in _relevant_subdivisions:
        # the method __add__ expects a Union[int, "HolidayBase", "HolidaySum"] as `other`
        # here, we're dealing with a child instance of HolidayBase
        result += Germany(
            subdiv=subdivision, observed=False, language="de"
        )  # type: ignore[assignment]
    if result.language is None:
        # This is a workaround to a problem in holidays 0.20-0.53 (at least):
        # When adding the subdivisions, the language attribute is lost,
        # although holiday base and subdivision share the same language.
        # The problem happens here:
        # https://github.com/vacanza/python-holidays/blob/v0.53/holidays/holiday_base.py#L1164
        result.language = original_language_before_adding_subdivisions
    return result


__all__ = ["BdewDefinedHolidays", "create_bdew_calendar"]
