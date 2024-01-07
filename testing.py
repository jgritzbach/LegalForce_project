"""
This module serves as a playground and a test lab for evolving code
"""

from legal_force import LegalForce
import datetime as dt

lf = LegalForce()
print(lf.is_weekend(dt.date(2024,1,6)))