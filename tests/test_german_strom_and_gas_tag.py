from datetime import datetime, timedelta, timezone

import pytest

from bdew_datetimes.enums import Division
from bdew_datetimes.german_strom_and_gas_tag import (
    has_no_utc_offset,
    is_gastag_limit,
    is_stromtag_limit,
    is_xtag_limit,
)
from bdew_datetimes.german_time_zone import GERMAN_TIME_ZONE


@pytest.mark.parametrize(
    "dt, expected_is_start_or_end_of_german_stromtag",
    [
        pytest.param(
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc), False
        ),
        pytest.param(
            datetime(2019, 12, 31, 23, 0, 0, tzinfo=timezone.utc), True
        ),
        pytest.param(
            datetime(2019, 12, 31, 22, 0, 0, tzinfo=timezone.utc), False
        ),
        pytest.param(
            datetime(2010, 1, 1, 0, 0, 0, tzinfo=GERMAN_TIME_ZONE), True
        ),
        pytest.param(
            datetime(
                2010, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
            ),
            True,
        ),
        pytest.param(
            datetime(2022, 3, 26, 23, 0, 0, 0, tzinfo=timezone.utc), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-03-27T00:00:00+01:00"), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-03-27T00:00:00+02:00"), False
        ),
        pytest.param(
            datetime(2022, 3, 27, 22, 0, 0, 0, tzinfo=timezone.utc), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-03-28T00:00:00+02:00"), True
        ),
        pytest.param(
            datetime(2022, 10, 29, 22, 0, 0, 0, tzinfo=timezone.utc), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-30T00:00:00+02:00"), True
        ),
        pytest.param(
            datetime(2022, 10, 30, 23, 0, 0, 0, tzinfo=timezone.utc), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-31T00:00:00+01:00"), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-31T00:00:00+02:00"), False
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-29T12:00:00-10:00"),
            True,
            id="Hawaii, German DST",
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-30T13:00:00-10:00"),
            True,
            id="Hawaii, German standard time",
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-30T07:00:00+09:00"),
            True,
            id="Tokyo, German DST",
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-31T08:00:00+09:00"),
            True,
            id="Tokyo, German standard time",
        ),
    ],
)
def test_stromtag(
    dt: datetime, expected_is_start_or_end_of_german_stromtag: bool
) -> None:
    actual = is_stromtag_limit(dt)
    assert actual == expected_is_start_or_end_of_german_stromtag


@pytest.mark.parametrize(
    "dt, expected_is_start_or_end_of_german_gastag",
    [
        pytest.param(
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc), False
        ),
        pytest.param(datetime(2020, 1, 1, 5, 0, 0, tzinfo=timezone.utc), True),
        pytest.param(
            datetime(2020, 1, 1, 4, 0, 0, tzinfo=timezone.utc), False
        ),
        pytest.param(
            datetime(2022, 3, 26, 5, 0, 0, 0, tzinfo=timezone.utc), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-03-26T06:00:00+01:00"), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-03-27T04:00:00+02:00"), False
        ),
        pytest.param(
            datetime(2022, 3, 27, 4, 0, 0, 0, tzinfo=timezone.utc), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-03-27T06:00:00+02:00"), True
        ),
        pytest.param(
            datetime(2022, 10, 29, 4, 0, 0, 0, tzinfo=timezone.utc), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-30T06:00:00+01:00"), True
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-30T06:00:00+02:00"), False
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-29T19:00:00-10:00"),
            True,
            id="Hawaii, German DST",
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-30T19:00:00-10:00"),
            True,
            id="Hawaii, German standard time",
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-29T09:45:00+05:45"),
            True,
            id="Nepal, German DST",
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-30T10:45:00+05:45"),
            True,
            id="Nepal, German standard time 1",
        ),
        pytest.param(
            datetime.fromisoformat("2022-10-31T10:45:00+05:45"),
            True,
            id="Nepal, German standard time 2",
        ),
    ],
)
def test_gastag(
    dt: datetime, expected_is_start_or_end_of_german_gastag: bool
) -> None:
    actual = is_gastag_limit(dt)
    assert actual == expected_is_start_or_end_of_german_gastag


@pytest.mark.parametrize(
    "dt, expected_has_not_utc_offset",
    [
        pytest.param(datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc), True),
        pytest.param(
            datetime.fromisoformat("2022-03-26T06:00:00+01:00"), False
        ),
        pytest.param(
            datetime.fromisoformat("2022-03-27T04:00:00+02:00"), False
        ),
    ],
)
def test_has_no_utc_offset(
    dt: datetime, expected_has_not_utc_offset: bool
) -> None:
    actual = has_no_utc_offset(dt)
    assert actual == expected_has_not_utc_offset


@pytest.mark.parametrize(
    "dt, division",
    [
        pytest.param(datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc), 0),
    ],
)
def test_is_xtag_limit_raises(dt: datetime, division: Division) -> None:
    with pytest.raises(NotImplementedError):
        is_xtag_limit(date_time=dt, division=division)


@pytest.mark.parametrize(
    "dt, division, expected",
    [
        pytest.param(
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            Division.GAS,
            False,
        ),
        pytest.param(
            datetime(2020, 1, 1, 5, 0, 0, tzinfo=timezone.utc),
            Division.GAS,
            True,
        ),
        pytest.param(
            datetime(2020, 1, 1, 4, 0, 0, tzinfo=timezone.utc),
            Division.GAS,
            False,
        ),
        pytest.param(
            datetime(2022, 3, 26, 5, 0, 0, 0, tzinfo=timezone.utc),
            Division.GAS,
            True,
        ),
        pytest.param(
            datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            Division.STROM,
            False,
        ),
        pytest.param(
            datetime(2019, 12, 31, 23, 0, 0, tzinfo=timezone.utc),
            Division.STROM,
            True,
        ),
        pytest.param(
            datetime(2019, 12, 31, 22, 0, 0, tzinfo=timezone.utc),
            Division.STROM,
            False,
        ),
        pytest.param(
            datetime(2010, 1, 1, 0, 0, 0, tzinfo=GERMAN_TIME_ZONE),
            Division.STROM,
            True,
        ),
    ],
)
def test_is_xtag_limit(
    dt: datetime, division: Division, expected: bool
) -> None:
    actual = is_xtag_limit(dt, division)
    assert actual == expected
