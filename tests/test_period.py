from datetime import date

import pytest  # type:ignore[import]

from bdew_datetimes.periods import (
    DayType,
    EndDateType,
    Period,
    _DayTyp,
    add_frist,
    get_next_working_day,
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
