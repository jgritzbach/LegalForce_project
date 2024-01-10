from datetime import date, datetime, timedelta
from dateutil import easter


class LegalForce:
    """
    a tool related to the computations of a legal force of court decisions in the Czech Republic
    """
    def __init__(self, given_date = None):
        """
        All computations are related to a given date, expected to be passed on creation. If omitted, today is passed.
        The given date is stored as instance property and can be changed later by setting the property on different date
        """
        if given_date is None:
            given_date = date.today()  # if date is not specified, it will be today

        self.given_date = given_date

    @property
    def given_date(self):
        """
        returns inner property of given date
        """
        return self.__given_date

    @given_date.setter
    def given_date(self, arg_date):
        """
        sets given date as inner property, if passed argument is valid date or datetime object. Otherwise TypeError
        by given date being passed once and stored in property, type validity needs to be checked just once
        """
        self.__given_date = self.__valid_date(arg_date)
        self.__holidays = self.czech_public_holidays()  # anytime given date is set, holidays are recalculated

    def is_weekend(self):
        """
        returns True if given date is saturday or sunday. Otherwise, returns False
        """

        return self.given_date.weekday() in {5, 6}

    def is_public_holiday(self):
        """
        returns True if given date is czech public holiday. Otherwise, returns False
        """

        return self.given_date in self.__holidays

    def is_workday(self):
        """
        returns True if given date is ordinary workday. Otherwise, returns False
        """

        return not (self.is_weekend() or self.is_public_holiday())

    def czech_public_holidays(self):
        """returns a list of public holidays in the Czech Republic for a given year

        :param year: a year is needed to determine the Easter. Omitting the year results in current year being used.
        :return: a list of datetime.date objects
        """
        year = self.given_date.year
        easter_date = easter.easter(year)

        holidays = [
            date(year, 1, 1),  # New year
            easter_date + timedelta(-2),  # Good friday
            easter_date + timedelta(1),  # Easter monday
            date(year, 5, 1),  # Labor day
            date(year, 5, 1),  # Day of liberation of Czechoslovakia
            date(year, 7, 5),  # Day of the Slavic Apostles Cyril and Methodius
            date(year, 7, 6),  # Day of the Burning of Master Jan Hus
            date(year, 9, 28),  # Day of Czech Statehood
            date(year, 10, 28),  # Day of the Establishment of the Independent Czechoslovak State
            date(year, 11, 17),  # Day of Struggle for Freedom and Democracy
            date(year, 12, 24),  # Christmas Eve
            date(year, 12, 25),  # First Day of Christmas
            date(year, 12, 26),  # Second Day of Christmas
            date(year + 1, 1, 1),  # next New year -> since appeal window is just 15 days and no other public
        ]                                       # holiday falls on January, this is enough

        return holidays

    def __valid_date(self, date_to_test):
        """
        raises TypeError if passed argument is not an instance of either datetime.date or datetime.datetime object
        otherwise returns the passed argument intact
        """
        if not (isinstance(date_to_test, date) or isinstance(date_to_test, datetime)):
            raise TypeError

        return date_to_test
