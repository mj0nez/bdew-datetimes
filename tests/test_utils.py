import pytest
from syrupy.assertion import SnapshotAssertion

from bdew_datetimes import (
    get_all_bdew_non_working_days,
    get_all_bdew_working_days,
)


@pytest.mark.snapshot
def test_get_non_working_days_2026_without_weekends(
    snapshot: SnapshotAssertion,
) -> None:
    non_working_days = get_all_bdew_non_working_days(
        2026, include_weekends=False
    )
    snapshot.assert_match(non_working_days)


@pytest.mark.snapshot
def test_get_non_working_days_2026_including_weekends(
    snapshot: SnapshotAssertion,
) -> None:
    non_working_days = get_all_bdew_non_working_days(
        2026, include_weekends=True
    )
    snapshot.assert_match(non_working_days)


@pytest.mark.snapshot
def test_get_working_days(snapshot: SnapshotAssertion) -> None:
    non_working_days = get_all_bdew_working_days(2026)
    snapshot.assert_match(non_working_days)
