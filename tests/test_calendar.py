from datetime import date, datetime

import pytest  # type:ignore[import]
from holidays import DateLike

from bdew_datetimes.calendar import BdewDefinedHolidays, create_bdew_calendar


@pytest.mark.parametrize(
    "expected_holiday",
    [
        pytest.param(date(2021, 12, 31), id="Silvester 2021"),
        pytest.param(date(2021, 12, 24), id="Heiligabend 2021"),
        pytest.param(date(2070, 12, 31), id="arbitrary Silvester"),
        pytest.param(date(2070, 12, 24), id="arbitrary Heiligabend"),
    ],
)
def test_bdew_holidays(expected_holiday: date):
    calendar = BdewDefinedHolidays()
    assert expected_holiday in calendar


@pytest.mark.parametrize(
    "test_date, expected_is_in_calendar",
    [
        pytest.param(date(2021, 12, 31), True, id="Silvester 2021 (BDEW)"),
        pytest.param(date(2022, 1, 1), True, id="Neujahr 2022 (bundesweit)"),
        pytest.param(date(2022, 1, 2), False, id="a regular Sunday"),
        pytest.param(date(2022, 8, 15), True, id="Mariä Himmelfahrt (BY, SL)"),
    ],
)
def test_create_bdew_calendar(test_date: date, expected_is_in_calendar: bool):
    calendar = create_bdew_calendar()
    if expected_is_in_calendar:
        assert test_date in calendar
    else:
        assert test_date not in calendar


def test_holiday_calendar_obj():
    calendar = create_bdew_calendar()

    assert not calendar.observed
    assert calendar.country == "DE"


@pytest.mark.parametrize(
    "candidate",
    [
        pytest.param(datetime(2022, 1, 1, 22, 16, 59)),
        pytest.param("2022-01-01"),
        pytest.param("1/1/2022"),
        pytest.param(
            datetime(2022, 1, 1, 22, 16, 59).timestamp(),
            id="POSIX timestamp: 1641071819.0",
        ),
        pytest.param(int(datetime(2022, 1, 1, 22, 16, 59).timestamp())),
    ],
)
def test_holiday_in_calendar(candidate: DateLike):
    calendar = create_bdew_calendar()
    assert candidate in calendar
