from datetime import date, datetime, timedelta
from dateutil import easter
import string


class LegalForceManager:
    """Serves for user interaction with the LegalForce class

    LegalForce class itself can be used for calculations alone by other parts of your program, not relying on user.
    However, with this manager, it can be used to compute legal force by interacting with the user
    """

    @staticmethod
    def interact():
        """Prompts user to enter date as string. Returns the date of legal force counted from the given date

        Method works in cycle, so that as many consecutive dates can be entered as needed.
        This is useful, since it is very common technique for court officers to count many legal force dates at once.
        """

        print('\nWelcome to interactive calculator of legal force!\n')
        print(("Fill in the date of successful delivery of the court decision \n"
               "to the last party with the right to appeal.\n"
               "(or keep blank and press ENTER to quit)\n"))

        quit_by = {"", "q", 0, "quit", "quit()", "exit", "exit()", "abort", "abort()", }
        allowed_formats = ["%y-%m-%d", "%Y-%m-%d", "%y.%m.%d", "%Y.%m.%d", "%y,%m,%d", "%Y,%m,%d"]
        prompt = "\nfill in the date (y-m-d): "  # more formats are supported, although the prompt is brief at first
        user_input = True  # default input is True to start the cycle

        while user_input:

            # acquiring the input
            arg_date = None  # reset the date provided by the user in each cycle to enable
            user_input = input(prompt)
            user_input = ''.join(char for char in user_input if char not in string.whitespace)  # removing whitespaces

            # if user wants to quit
            if user_input.lower() in quit_by:  # any of the quiting phrase
                print('\nGoodbye!\n')
                break  # will end the cycle immediately

            # trying to construct date object from user input
            for allowed_format in allowed_formats:  # we iterate through allowed formats in a hope to find the match
                try:
                    arg_date = datetime.strptime(user_input, allowed_format).date()  # if the user input fits
                    break  # then the construction of date object was successful - we can stop the iteration

                except ValueError:  # if the iterated format did not succeed
                    continue  # let us try another one

            # here, the efforts to construct the date object from user input are over, successful or not

            if arg_date:  # if the date object was successfully constructed from the user input
                legal_force_date = LegalForce.legal_force(arg_date)  # we can pass it to LegalForce for calculation
                print(f'the date of the legal force: {legal_force_date}')  # and print it

                if legal_force_date > date.today():  # if date of the legal force lies in a future
                    print('Please note that this is a future date!')  # we remind the user

            else:  # if the user input did not fit any of the allowed formats, we notify the user
                print(f'\n{user_input} is an inappropriate date format!\n')
                print("use one of these formats:\n", "\n".join(allowed_formats), "\n", sep="")
                print('(or keep blank and press Enter to quit)\n')


class LegalForce:
    """
    A tool related to the computations of a legal force of court decisions in the Czech Republic
    """

    APPEAL_DEADLINE = 15  # appeal deadline is 15 days long since successfully delivery of the court decision

    @staticmethod
    def legal_force(arg_date):
        """
        Returns the moment of legal force based on a given date
        """
        arg_date += timedelta(LegalForce.APPEAL_DEADLINE)  # the last day of 15-day deadline
        arg_date = LegalForce.shift_to_workday(arg_date)  # which always has to end on an ordinary workday
        arg_date += timedelta(1)  # on the 1st day after appeal deadline, the court decision is legally binding

        return arg_date

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
        ]

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


if __name__ == "__main__":
    LegalForceManager.interact()    # if run directly, starts the interaction with the user
