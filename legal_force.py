from datetime import date, datetime, timedelta
from dateutil import easter


class LegalForce:
    """
    a tool related to the computations of a legal force of court decisions in the Czech Republic
    """

    def __init__(self, given_date=None):
        """
        all computations are related to a given date, expected to be passed on creation. If omitted, today is passed.
        The given date is stored as instance property and can be changed later by setting the property on different date
        """
        # date validation and holiday recalculation are flags that can be turned off
        self.__validate_dates = True  # date validation may be skipped (f.e. iterations of previously checked date)
        self.__recalculate_holidays = True  # recalculating holidays may be skipped for the same reason

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
        sets given date as inner property, if passed argument is valid date or datetime object. Otherwise, TypeError
        by given date being passed once and stored in property, type validity needs to be checked just once
        """

        # anytime given date is to be set, arg_date is validated and holidays are recalculated, unless turned off

        self.__given_date = self.__valid_date(arg_date) if self.__validate_dates else arg_date

        if self.__recalculate_holidays:
            self.__set_holidays()

    def is_workday(self):
        """
        returns True if given date is ordinary workday. Otherwise, returns False
        """

        return not (self.is_weekend() or self.is_public_holiday())

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

    def shift_to_workday(self):
        """
        shifts given date to the nearest workday, if not workday already, and returns the given date
        """
        # we temporarily disable date validation and holiday recalculation
        # since given date is manipulated by timedelta, we can be sure that date type is still valid
        # since just one day per each iteration is added, recalculating holiday for the whole year is not necessary
        self.__validate_dates = False
        self.__recalculate_holidays = False

        try:
            # since consecutive holidays can occur in the Cezch republic, using while cycle is the most straighforward
            while not self.is_workday():
                self.given_date += timedelta(1)
        finally:  # even if something ever goes wrong, we always at least
            self.__validate_dates = True  # turn back on the date validation
            self.__recalculate_holidays = True  # holiday recalculation

        self.__set_holidays()  # since holiday recalculation was turned off, we recalculate now
        return self.given_date

    def czech_public_holidays(self):
        """
        returns a list of date objects of public holidays in the Czech Republic for a year relevant to the given date
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
        raises TypeError if passed argument is not an instance of either date or datetime object
        otherwise returns the passed argument intact
        """
        if not (isinstance(date_to_test, date) or isinstance(date_to_test, datetime)):
            raise TypeError

        return date_to_test

    def __set_holidays(self):
        """calculates holidays relevant to the year of the given date and sets them as instance inner parameter
        """
        self.__holidays = self.czech_public_holidays()
