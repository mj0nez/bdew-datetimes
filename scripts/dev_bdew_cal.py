import holidays
from datetime import date

from holidays.countries.germany import BDEWCalender


def print_info(calendar):

    print(f"{calendar.country=} {calendar.subdiv=}: {calendar.years}\n")


def main():
    germany = holidays.Germany

    germany = holidays.country_holidays(country="DE")
    saxonia = holidays.country_holidays(country="DE", subdiv="SN")
    bavaria = holidays.country_holidays(country="DE", subdiv="BY")

    comby = germany + saxonia + bavaria
    comby_wo_sax = germany + bavaria

    cals = (germany, saxonia, bavaria, comby, comby_wo_sax)

    for x in cals:

        print_info(x)

    print(comby)


    is_holiday_in_ger = date(2022, 10, 31) in germany
    is_holiday_in_sax = date(2022, 10, 31) in saxonia
    is_holiday_in_bav = date(2022, 10, 31) in bavaria
    is_holiday_in_bdew = date(2022, 10, 31) in comby
    is_holiday_w0_sax = date(2022, 10, 31) in comby_wo_sax

    bdew = BDEWCalender()

    print_info(bdew)
    print(date(2022,12,31) in bdew)
    print(date(2022,12,31) in germany)



    print()

    calendar = create_bdew_calendar()

    print(calendar)
    print(date(2022,10,31) in calendar)
    print(date(2022,11,1) in calendar)

    print(calendar)
    print(calendar.years)
    print(date(2023,11,1) in calendar)
    print(calendar.years)


def create_bdew_calendar() -> holidays.HolidaySum:

    calendar = BDEWCalender()

    for cal in calendar.subdivisions:
        calendar += holidays.country_holidays(country=calendar.country, subdiv=cal)

    print_info(calendar)
    
    return calendar

if __name__ == "__main__":
    main()
