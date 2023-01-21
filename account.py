"""This module creates a bank account"""

import random


class Account:
    """This method create a bank account."""
    def __init__(self, user, interest=0):
        self.account_number = random.randint(1000000000, 9999999999)
        self.account_holder = user
        self.credit_balance = 0
        self.interest = interest

    def deposit(self, money):
        """Function to pay money on a account."""
        self.credit_balance = round(self.credit_balance + money, 2)

    def withdraw(self, money):
        """Function to take money from account."""
        self.credit_balance = round(self.credit_balance - money, 2)



