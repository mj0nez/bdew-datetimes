"""enums used inside the package"""

from enum import Enum


class Division(Enum):
    """
    Allows to distinguish divisions used by German utilities, German "Sparte".
    """

    STROM = 1  #: electricity
    GAS = 2  #: gas


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
    If a contract ends with the year 2022 and the end date is denoted as "2023-01-01",
    then the end date is exclusive. Most end dates handled by technical systems are meant
    exclusively.
    """


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


__all__ = ["Division", "EndDateType", "MonthType", "DayType"]
