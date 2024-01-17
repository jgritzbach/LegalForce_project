# THE LEGAL FORCE PROJECT

## Welcome to the LegalForce project! 

The LegalForce project is a tool related to the ***computations of a legal force of court decisions*** in the Czech Republic.
It is a custom project crafted by a self-taught developer who also happens to be a senior court officer in the Czech Republic. Feel free to raise any issue about the code quality and suggest improvements!


## Main idea

In the Czech Republic, when a court issues a resolution, the parties can appeal against the resolution (unless the specific type of resolution prevents it). Only when this appeal opportunity is lost (or when the appeal itself is not successful) the court decision will become legally binding. 

We say that the court decision is in the state of legal force. Czech laws provide a 15-day time window for the appeal. 
This period starts from the day of the successful delivery of the court decision to the party. However, should the 15-day period end during a weekend or public holiday, the end of the period shifts to the next workday.

**Calculating the date of the legal force manually can be tricky**. It is cumbersome and error-prone, especially around public holidays that shift the end of the appeal deadline. Since the easter date is different each year, it can come as a factor of human error.

This project should help you calculate the moment of legal force despite complications with weekends and Czech public holidays including easter.

## Usage

The module logic is split into two main classes:
1) ***LegalForce*** class performs the calculations
2) ***LegalForceManager*** class serves for direct user interactions

***LegalForce*** class is a relatively independent part of the project serving merely for computations. This class itself does not require any user interaction to function. You can use it simply as a calculation tool for your other programs. For example, you can use it to count legal force dates for a large dataset of dates from your database. The main method here is *legal_force()* which accepts a date object and calculates the date of the legal force since this date.

***LegalForceManager*** class communicates with the user through CLI and prompts him to input a date. It then uses the LegalForce class to calculate the date of the legal force and prints it back to the console. It repeats the cycle until the user decides to quit. The main method here is *interact()* to start the interaction with the user through CLI. The interactive mode with its cyclical nature is useful for court officers since it is a very common technique for them to calculate many legal force dates at once, after they pile up in their office. 

**If you run the legal_force.py module directly** by __python -m legal_force__ command, you will enter *the interactive mode* of LegalForceManager.

## Requirements

Please note that you will need a *python3 interpreter* (see https://www.python.org/) and *python-dateutil* library installed (simply write 'pip install python-dateutil' without the quotation marks into your console). See *requirements.txt*.


## Issues 

I hope you will find this project useful!
If you don't or if you have trouble with using it, please suggest an improvement, either here in issues or via my email jgritzbach@gmail.com


