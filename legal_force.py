from datetime import date, datetime, timedelta
from dateutil import easter

class LegalForce:

    def is_weekend(self, given_date):
        """
        returns true if given date is saturday or sunday. Otherwise, returns false
        """
        if self.__valid_date(given_date):
            return given_date.weekday() in {5, 6}
        raise TypeError

    def is_public_holiday(self, given_date):
        """
        returns true if given date is czech public holiday. Otherwise, returns false
        """
        if self.__valid_date(given_date):
            return given_date in self.__czech_public_holidays()
        raise TypeError

    def __valid_date(self, date_to_test):
        """
        return true if argument is either datetime.date or datetime.datetime object
        """

        return isinstance(date_to_test,date) or isinstance(date_to_test,datetime)

    def __czech_public_holidays(self, year = None):
        """returns a list of public holidays in the Czech Republic for a given year

        :param year: a year is needed to determine the Easter. Omitting the year results in current year being used.
        :return: a list of datetime.date objects
        """
        if year == None:
            year = date.today().year

        easter_date = easter.easter(year)

        holidays = [
        date(year, 1, 1),  # New year
        easter_date + timedelta(-2),  # Good friday
        easter_date + timedelta(1),  # Easter monday
        date(year, 5, 1),  # Labor day
        date(year, 5, 1),  # Day of liberation of Czechoslovakia
        date(year, 7 ,5),  # Day of the Slavic Apostles Cyril and Methodius
        date(year, 7, 6),  # Day of the Burning of Master Jan Hus
        date(year, 9, 28),  # Day of Czech Statehood
        date(year, 10, 28),  # Day of the Establishment of the Independent Czechoslovak State
        date(year, 11, 17),  # Day of Struggle for Freedom and Democracy
        date(year, 12, 24),  # Christmas Eve
        date(year, 12, 25),  # First Day of Christmas
        date(year, 12, 26),  # Second Day of Christmas
        ]

        return holidays
