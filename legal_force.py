import datetime as dt
class LegalForce:

    def is_weekend(self, date):
        """returns true given date is saturday or sunday. Otherwise returns false
        """
        if isinstance(date,dt.date) or isinstance(date,dt.datetime) :
            return date.weekday() in {5, 6}
        raise TypeError


