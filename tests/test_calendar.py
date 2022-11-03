from energy_datetime.calendar import BdewDefinedHolidays, create_bdew_calendar

from datetime import date, datetime


def test_bdew_holidays():
    calendar = BdewDefinedHolidays()

    assert date(2021, 12, 31) in calendar  # ensure silvester is valid
    assert date(2021, 12, 24) in calendar  # ensure silvester is valid


def test_create_bdew_calendar():

    calendar = create_bdew_calendar()

    assert date(2021, 12, 31) in calendar  # ensure silvester is valid

    assert date(2022, 1, 1) in calendar
    assert date(2022, 1, 2) not in calendar

    # mariä himmelfahrt only in BY and SL
    assert date(2022, 8, 15) in calendar


def test_holiday_calendar_obj():

    calendar = create_bdew_calendar()

    assert not calendar.observed
    assert calendar.country == "DE"


def test_holiday_check():
    calendar = create_bdew_calendar()

    assert datetime(2022, 1, 1, 22, 16, 59) in calendar
    assert "2022-01-01" in calendar
    assert "1/1/2022" in calendar

    ts = datetime(
        2022, 1, 1, 22, 16, 59
    ).timestamp()  # POSIX timestamp: 1641071819.0

    assert ts in calendar
    assert int(ts) in calendar
