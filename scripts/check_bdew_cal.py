from holidays.countries.germany import Germany 
from datetime import date, datetime
from energy_datetime import create_bdew_calendar


if __name__ == "__main__":

    calendar = create_bdew_calendar()

    print(date(2022, 10, 31) in calendar)
    print(date(2022, 11, 1) in calendar)
    print(datetime(2022, 11, 1, 0, 1, 0) in calendar)

    print(calendar.observed)

    print(Germany().observed)


    print(date(2022,4,10) in calendar)