from datetime import date

import pytest  # type:ignore[import]

from bdew_datetimes.periods import (
    DayType,
    EndDateType,
    MonthType,
    Period,
    _DayTyp,
    add_frist,
    get_next_working_day,
    get_nth_working_day_of_month,
    get_previous_working_day,
)


def test_period_instantiation_with_enum():
    period = Period(42, DayType.WORKING_DAY)
    assert period.number_of_days == 42
    assert period.day_type == DayType.WORKING_DAY


def test_period_instantiation_with_enum_and_inclusive_end():
    period = Period(
        42, DayType.WORKING_DAY, end_date_type=EndDateType.INCLUSIVE
    )
    assert period.number_of_days == 41
    assert period.day_type == DayType.WORKING_DAY


@pytest.mark.parametrize(
    "number_of_days, str_daytype, expected",
    [
        pytest.param(42, "WT", Period(42, DayType.WORKING_DAY)),
        pytest.param(17, "KT", Period(17, DayType.CALENDAR_DAY)),
    ],
)
def test_period_instantiation_with_str(
    number_of_days: int, str_daytype: _DayTyp, expected: Period
):
    actual = Period(number_of_days, str_daytype)
    assert actual == expected


def test_instantiation_with_invalid_str():
    with pytest.raises(ValueError):
        _ = Period(
            42, "Foo"  # type:ignore[argument] # literal is intentionally wrong
        )


@pytest.mark.parametrize(
    "start,expected",
    [
        pytest.param(
            date(2023, 1, 1),
            date(2023, 1, 2),
        ),
        pytest.param(
            date(2023, 1, 2), date(2023, 1, 3), id="regular next working day"
        ),
        pytest.param(
            date(2023, 1, 5),
            date(2023, 1, 9),
            id="Skip Hl.drei Könige (subdivision holiday) and weekend",
        ),
        pytest.param(
            date(2022, 12, 30),
            date(2023, 1, 2),
            id="Skip Silvester (BDEW) and Neujahr (federal) holidays",
        ),
    ],
)
def test_get_next_working_day(start: date, expected: date):
    actual = get_next_working_day(start)
    assert actual == expected


@pytest.mark.parametrize(
    "start,expected",
    [
        pytest.param(
            date(2023, 1, 1),
            date(2022, 12, 30),
        ),
        pytest.param(
            date(2023, 1, 3),
            date(2023, 1, 2),
            id="regular previous working day",
        ),
        pytest.param(
            date(2023, 1, 9),
            date(2023, 1, 5),
            id="Skip Hl.drei Könige (subdivision holiday) and weekend",
        ),
    ],
)
def test_get_previous_working_day(start: date, expected: date):
    actual = get_previous_working_day(start)
    assert actual == expected


@pytest.mark.parametrize(
    "start,frist,expected",
    [
        pytest.param(
            date(2023, 1, 1),
            Period(0, DayType.CALENDAR_DAY),
            date(2023, 1, 2),
            id="+0 KT is the next day if start is a holiday",
        ),
        pytest.param(
            date(2023, 1, 2),
            Period(0, DayType.CALENDAR_DAY),
            date(2023, 1, 3),
            id="+0 KT is the next working day if start is a working day",
        ),
        pytest.param(
            date(2023, 1, 1),
            Period(0, DayType.WORKING_DAY),
            date(2023, 1, 2),
            id="+0 WT days is next (working) day if start is a holiday",
        ),
        pytest.param(
            date(2023, 1, 1),
            Period(1, DayType.CALENDAR_DAY),
            date(2023, 1, 3),
            id="+1 KT is day after next working day if start is a holiday",
        ),
        pytest.param(
            date(2023, 1, 3),
            Period(-1, DayType.CALENDAR_DAY),
            date(2023, 1, 2),
            id="-1 KT is day before working day if start is a holiday",
        ),
        pytest.param(
            date(2023, 1, 2),
            Period(1, DayType.CALENDAR_DAY),
            date(2023, 1, 4),
            id="+1 KT is day after next working day if start is a working day",
        ),
        pytest.param(
            date(2023, 1, 1),
            Period(1, DayType.WORKING_DAY),
            date(2023, 1, 3),
            id="BDEW Holiday + 1 working day is start",
        ),
        pytest.param(
            # From the Fristenberechnung-Chapter in the GPKE document:
            # "Lieferende bei Lieferantenwechselvorgängen:
            # Eingang der Abmeldung des LFA erfolgt am 04.07.2016. Der Mindestzeitraum von sechs WT beginnt am
            # 05.07.2016 und endet am 12.07.2016. Frühestes zulässiges Abmeldedatum ist damit der 12.07.2016 [...]."
            date(2016, 7, 4),
            Period(
                6,
                DayType.WORKING_DAY,
                end_date_type=EndDateType.INCLUSIVE
                # the abmeldedatum is the inclusive end of a contract
            ),
            date(2016, 7, 12),
            id="Lieferende bei Lieferantenwechselvorgängen",
        ),
        pytest.param(
            date(2016, 7, 12),
            Period(
                -6,
                DayType.WORKING_DAY,
                end_date_type=EndDateType.INCLUSIVE
                # the abmeldedatum is the inclusive end of a contract
            ),
            date(2016, 7, 4),
            id="revert 'Lieferende bei Lieferantenwechselvorgängen'",
        ),
        pytest.param(
            # Eingang der Anmeldung des LFN erfolgt am 04.07.2016. Der Mindestzeitraum von sieben bzw. zehn WT
            # beginnt am 05.07.2016 und endet am 13.07.2016 bzw. 18.07.2016. Frühestes zulässiges Anmeldedatum
            # ist damit der 14.07.2016 bzw. 19.07.2016, sodass die Marktlokation dem LFN frühestens zum Beginn
            # des vorgenannten Tages zugeordnet wird.
            date(2016, 7, 4),
            Period(
                7,
                DayType.WORKING_DAY,
                end_date_type=EndDateType.EXCLUSIVE
                # lieferbeginn is the exclusive end of the previous contract
            ),
            date(2016, 7, 14),
            id="Lieferbeginn bei Lieferantenwechselvorgängen (7WT)",
        ),
        pytest.param(
            date(2016, 7, 14),
            Period(
                -7,
                DayType.WORKING_DAY,
                end_date_type=EndDateType.EXCLUSIVE
                # lieferbeginn is the exclusive end of the previous contract
            ),
            date(2016, 7, 4),
            id="revert 'Lieferbeginn bei Lieferantenwechselvorgängen' (-7WT)",
        ),
        pytest.param(
            # Eingang der Anmeldung des LFN erfolgt am 04.07.2016. Der Mindestzeitraum von sieben bzw. zehn WT
            # beginnt am 05.07.2016 und endet am 13.07.2016 bzw. 18.07.2016. Frühestes zulässiges Anmeldedatum
            # ist damit der 14.07.2016 bzw. 19.07.2016, sodass die Marktlokation dem LFN frühestens zum Beginn
            # des vorgenannten Tages zugeordnet wird.
            date(2016, 7, 4),
            Period(
                10,
                DayType.WORKING_DAY,
                end_date_type=EndDateType.EXCLUSIVE
                # lieferbeginn is the exclusive end of the previous contract
            ),
            date(2016, 7, 19),
            id="Lieferbeginn bei Lieferantenwechselvorgängen (10WT)",
        ),
        pytest.param(
            date(2016, 7, 19),
            Period(
                -10,
                DayType.WORKING_DAY,
                end_date_type=EndDateType.EXCLUSIVE
                # lieferbeginn is the exclusive end of the previous contract
            ),
            date(2016, 7, 4),
            id="revert 'Lieferbeginn bei Lieferantenwechselvorgängen' (-10WT)",
        ),
    ],
)
def test_add_frist(start: date, frist: Period, expected: date):
    actual = add_frist(start, frist)
    assert actual == expected


@pytest.mark.parametrize(
    "number,start,month_type,expected",
    [
        pytest.param(
            14,
            date(2023, 1, 1),
            MonthType.LIEFERMONAT,
            date(2023, 1, 20),
            id="14ter Werktag des (Liefer)Monats Januar 203; BK-Summen",
        ),
        pytest.param(
            16,
            date(2023, 1, 1),
            MonthType.LIEFERMONAT,
            date(2023, 1, 24),
            id="16ter Werktag des (Liefer)Monats Januar 2023; Zuordnungslisten",
        ),
        pytest.param(
            17,
            date(2023, 1, 1),
            MonthType.LIEFERMONAT,
            date(2023, 1, 25),
            id="17ter Werktag des (Liefer)Monats Januar 2023; BK-Zuordnungsliste, Deklarationsliste",
        ),
        pytest.param(
            18,
            date(2023, 11, 1),
            MonthType.LIEFERMONAT,
            date(2023, 11, 28),
            id="18ter Werktag des (Liefer)Monats November 2023; Deklarationsmitteilung",
        ),
        pytest.param(
            14,
            date(2023, 2, 1),
            MonthType.LIEFERMONAT,
            date(2023, 2, 20),
            id="14ter Werktag des (Liefer)Monats Februar 2023; BK-Summen",
        ),
        pytest.param(
            16,
            date(2023, 2, 1),
            MonthType.LIEFERMONAT,
            date(2023, 2, 22),
            id="16ter Werktag des (Liefer)Monats Februar 2023; Zuordnungslisten",
        ),
        pytest.param(
            17,
            date(2023, 2, 1),
            MonthType.LIEFERMONAT,
            date(2023, 2, 23),
            id="17ter Werktag des (Liefer)Monats Februar 2023; BK-Zuordnungsliste, Deklarationsliste",
        ),
        pytest.param(
            18,
            date(2023, 2, 1),
            MonthType.LIEFERMONAT,
            date(2023, 2, 24),
            id="18ter Werktag des (Liefer)Monats Februar 2023; Deklarationsmitteilung",
        ),
        pytest.param(
            21,
            date(2023, 1, 1),
            MonthType.FRISTENMONAT,
            date(2023, 3, 1),
            id="21ter Werktag des Fristenmonats Januar 2023;",
        ),
        pytest.param(
            21,
            date(2023, 2, 1),
            MonthType.FRISTENMONAT,
            date(2023, 3, 30),
            id="21ter Werktag des Fristenmonats Februar; NKP",
        ),
        pytest.param(
            26,
            date(2022, 12, 1),
            MonthType.FRISTENMONAT,
            date(2023, 2, 7),
            id="26ter Werktag des Fristenmonats Dezember 2022",
        ),
        pytest.param(
            26,
            date(2023, 1, 1),
            MonthType.FRISTENMONAT,
            date(2023, 3, 9),
            id="26ter Werktag des Fristenmonats Januar 2023",
        ),
        pytest.param(
            26,
            date(2023, 6, 1),
            MonthType.FRISTENMONAT,
            date(2023, 8, 7),
            id="26ter Werktag des Fristenmonats Juni 2023; NKP MG-Überlappung",
        ),
        pytest.param(
            30,
            date(2023, 4, 1),
            MonthType.FRISTENMONAT,
            date(2023, 6, 15),
            id="30ter Werktag des Fristenmonats April 2023; letztmalige Datenabnahme beim BIKO",
        ),
        pytest.param(
            42,
            date(2022, 11, 1),
            MonthType.FRISTENMONAT,
            date(2023, 1, 31),
            id="42ter Werktag des Fristenmonats November 2022; BK-Abrechnung",
        ),
        pytest.param(
            42,
            date(2023, 7, 1),
            MonthType.FRISTENMONAT,
            date(2023, 9, 29),
            id="42ter Werktag des Fristenmonats Juli 2023; BK-Abrechnung",
        ),
    ],
)
def test_get_nth_working_day_of_month(
    number: int, start: date, month_type: MonthType, expected: date
):
    actual = get_nth_working_day_of_month(number, month_type, start)
    assert actual == expected
