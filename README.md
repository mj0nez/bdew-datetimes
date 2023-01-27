# bdew_datetimes

A collection of utils to work with datetimes and holidays in the German energy
market and is based on the [python-holiday](https://github.com/dr-prodigy/python-holidays) package.

The implementation considers the publications of the **BDEW** (Bundesverband der Energie- und Wasserwirtschaft e. V.) and **EDI@Energy**, which provide boundaries and guidance for the data exchange on the german energy market. 

### Current highlights:
* BDEW-holiday calendar
    * allows dict like evaluation of dates and datetimes and contains all holidays considered by the BDEW
* Gas-Day / Market Day evaluation

### Future Scope:

* providing subdivision holiday calendars to allow granular load profiles


## Quick Start

```python
from datetime import date
from bdew_datetimes import create_bdew_calendar

bdew_holidays = create_bdew_calendar()  # this is a dict

assert date(2022, 12, 31) in bdew_holidays
assert not date(2022, 12, 2) in bdew_holidays

bdew_holidays.get('2022-01-01')  # "Neujahr"
```

Extending the `holidays` package, the `bdew_holidays` dict-like object will also recognize datetimes, date strings and Unix timestamps:

```python
import bdew_holidays
from datetime import datetime

assert datetime(2022, 1, 1, 22, 16, 59) in bdew_holidays
assert "2022-01-01" in bdew_holidays
assert "1/1/2022" in bdew_holidays

ts = datetime(2022, 1, 1, 22, 16, 59).timestamp()  # POSIX timestamp: 1641071819.0

assert ts in bdew_holidays
assert int(ts) in bdew_holidays  
```
## Notes

The BDEW considers all days as holidays, which are nationwide holidays and days, which are a holiday in at least one state.
Furthermore, the 24. and the 31. December are holidays as well.
Therefore, this package utilizes a composition of all available german holiday calendars amd adds the two additional days.

Shifting holidays to the next weekday if they fall on a weekend is currently not considered.  


## License

This library is licensed under the *MIT* license, see the [LICENSE file](LICENSE).
