from datetime import datetime, timezone

import pytest  # type:ignore[import]

from bdew_datetimes.times import has_no_utc_offset


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
def test_has_no_utc_offset(dt: datetime, expected_has_not_utc_offset: bool):
    actual = has_no_utc_offset(dt)
    assert actual == expected_has_not_utc_offset
