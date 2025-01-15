# bdew_datetimes
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/mj0nez/bdew-datetimes/packaging_test.yml?style=plastic)![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bdew-datetimes?style=plastic)![PyPI - License](https://img.shields.io/pypi/l/bdew-datetimes?style=plastic)![PyPI](https://img.shields.io/pypi/v/bdew-datetimes?style=plastic)

A collection of utils to work with datetimes and holidays in the German energy
market and is based on the [python-holiday](https://github.com/vacanza/holidays) package.

The implementation considers the publications of the **BDEW** (Bundesverband der Energie- und Wasserwirtschaft e. V.) and **EDI@Energy**, which provide boundaries and guidance for the data exchange on the german energy market. 

### Current highlights:
* BDEW-holiday calendar
    * allows dict like evaluation of dates and datetimes and contains all holidays considered by the BDEW
* Statutory Periods ("_Gesetzliche Fristen_")
    * calculate dates of the kind "_x Werktage ab Stichtag_"
    * calculate dates of the kind "_nter Werktag des Fristen- bzw. Liefermonats_"
* Gas-Day / Market Day evaluation

### Future Scope:

* providing subdivision holiday calendars to allow granular load profiles


## Quick Start and Examples

Install the package from [pypi](https://pypi.org/project/bdew-datetimes/):
```bash
pip install bdew-datetimes
```

### Check if a date is a _specific_ BDEW Holidays
> [!NOTE]  
By "specific" we mean: Holidays that are neither nation- nor statewide holidays (those are defined in the [upstream package holidays](https://github.com/vacanza/holidays)) but defined by the BDEW directly.
In 2025 those are: Sonderfeiertag 24h Lieferantenwechsel, Heiligabend and Silvester only.

The `HolidaySum` returned by `create_bdew_calendar` contains the BDEW specific holidays.
This means it contains those holidays which are _defined_ by BDEW which includes Heiligabend and Silvester as well as special days without Marktkommunikation but _not_ the local or nationwide holidays in Germany and its states. 
```python
from datetime import date
from bdew_datetimes import create_bdew_calendar

bdew_holidays = create_bdew_calendar()  # this behaves like a dict

assert date(2022, 12, 31) in bdew_holidays # Silvester is a BDEW holiday
assert date(2022, 8, 8) in bdew_holidays is False # Augsburger Friedensfest is _not_ a BDEW holiday (but a holiday in Augsburg only)
assert date(2022, 12, 2) in bdew_holidays is False # The 12th of February is not a BDEW holiday

print(bdew_holidays.get('2022-01-01'))  # prints "Neujahr"
```
The **union** (type `HolidaySum`) of both nation and state wide holidays **and** the BDEW holidays (only the latter is returned by `create_bdew_calendar`) is the relevant calendar for German utilities.

### Check if a given Date is a BDEW Working Day
BDEW working days are those days taken into account for the "Fristenberechnung".
The function `is_bdew_working_day` considers both national **and** state wide holidays **and** BDEW holidays:
```python
from datetime import date

from bdew_datetimes import is_bdew_working_day

assert is_bdew_working_day(date(2023, 1, 1)) is False  # Neujahr (national holiday)
assert is_bdew_working_day(date(2023, 1, 2)) is True  # regular weekday
assert is_bdew_working_day(date(2023, 1, 6)) is False  # Heilige Drei Könige (local holiday in parts of Germany)
assert is_bdew_working_day(date(2023, 4, 7)) is False  # Karfreitag (national holiday, but based on an astronomical calendar)
assert is_bdew_working_day(date(2023, 12, 24)) is False  # Heiligabend (BDEW holiday)
```

You can also get the next or previous working day for any date:
```python
from datetime import date

from bdew_datetimes import get_next_working_day, get_previous_working_day

assert get_next_working_day(date(2023, 1, 1)) == date(2023, 1, 2)  # the next working day after Neujahr
assert get_previous_working_day(date(2023, 1, 1)) == date(2022, 12, 30)  # the last working day of 2022
assert get_next_working_day(date(2023, 1, 20)) == date(2023, 1, 23)  # the next working day after a friday is the next monday
```

### Calculate Statutory Periods
Statutory periods define the maximum time between e.g. the EDIFACT message for the "Anmeldung" and the actual start of supply ("Lieferbeginn").

```python
from datetime import date

from bdew_datetimes import add_frist
from bdew_datetimes import Period
from bdew_datetimes.enums import DayType, EndDateType

# Eingang der Anmeldung des LFN erfolgt am 04.07.2016. Der Mindestzeitraum von zehn WT
# beginnt am 05.07.2016 und endet am 18.07.2016. Frühestes zulässiges Anmeldedatum
# ist damit der 19.07.2016, sodass die Marktlokation dem LFN frühestens zum Beginn
# des vorgenannten Tages zugeordnet wird.
eingang_der_anmeldung = date(2016, 7, 4)
gesetzliche_frist = Period(
  10,
  DayType.WORKING_DAY,
  end_date_type=EndDateType.EXCLUSIVE
  # lieferbeginn is the exclusive end of the previous supply contract
)
fruehest_moeglicher_lieferbeginn = add_frist(eingang_der_anmeldung, gesetzliche_frist)
assert fruehest_moeglicher_lieferbeginn == date(2016, 7, 19)
```
### Calculate "Liefer- and Fristenmonate"
Liefer- and Fristenmonat are concepts used in MaBiS and GPKE:

```python
from datetime import date

from bdew_datetimes import get_nth_working_day_of_month
from bdew_datetimes.enums import MonthType

# returns the 18th working day of the current month in Germany
get_nth_working_day_of_month(18)

# the 18th working day of November 2023
assert get_nth_working_day_of_month(18, start=date(2023, 11, 1)) == date(2023, 11, 28)

# the 42th working day of Fristenmonat July 2023
assert get_nth_working_day_of_month(42, month_type=MonthType.FRISTENMONAT, start=date(2023, 7, 1)) == date(2023, 9, 29)
```

## Notes

The BDEW considers all days as holidays, which are nationwide holidays and days, which are a holiday in at least one state.
Furthermore, the 24. and the 31. December are holidays as well.
Therefore, this package utilizes the composition of all available german holiday calendars and adds the two additional days.

Shifting holidays to the next weekday if they fall on a weekend is currently not considered.  


## License

This library is licensed under the *MIT* license, see the [LICENSE file](LICENSE).

## Users
This library is used by the following projects:
- [Hochfrequenz Fristenkalender](https://www.hochfrequenz.de/#fristenkalender)
