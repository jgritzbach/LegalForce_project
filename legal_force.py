from datetime import date, datetime, timedelta
from dateutil import easter


class LegalForce:
    """
    a tool related to the computations of a legal force of court decisions in the Czech Republic
    """

    def __init__(self):

        self.__APPEAL_DEADLINE = 15  # appeal deadline is 15 days long since successfully delivery of the court decision

    @staticmethod
    def is_weekend(arg_date):
        """
        returns True if given date is saturday or sunday. Otherwise, returns False
        """
        return arg_date.isoweekday() in {6, 7}

    @staticmethod
    def is_public_holiday(arg_date):
        """
        returns True if given date is czech public holiday. Otherwise, returns False
        """

        return arg_date in LegalForce.czech_public_holidays(arg_date.year)

    @staticmethod
    def is_workday(arg_date):
        """
        returns True if given date is ordinary workday. Otherwise, returns False
        """

        return not (LegalForce.is_weekend(arg_date) or LegalForce.is_public_holiday(arg_date))

    @staticmethod
    def shift_to_workday(arg_date):
        """
        shifts given date to the nearest ordinary workday, if not being ordinary workday already, and returns it
        """
        while not LegalForce.is_workday(arg_date):
            arg_date += timedelta(1)

        return arg_date

    @staticmethod
    def czech_public_holidays(year=None):
        """
        returns a list of date objects of public holidays in the Czech Republic for a year relevant to the given date
        if no year is passed, the current year is default
        """
        if year is None:
            year = date.today().year

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
            #date(year + 1, 1, 1),  # next New year -> since appeal window is just 15 days and no other public
        ]                                       # holiday falls on January, this is enough

        return holidays

    @staticmethod
    def valid_date(date_to_test):
        """
        raises TypeError if passed argument is not an instance of either date or datetime object
        otherwise returns the passed argument intact
        """
        if not (isinstance(date_to_test, date) or isinstance(date_to_test, datetime)):
            raise TypeError

        return date_to_test
