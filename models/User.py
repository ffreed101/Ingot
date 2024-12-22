import json

class User:
    def __init__(self, first, last, balance, fixed_expenses):
        self.first = first
        self.last = last
        self.balance = balance
        self.fixed_expenses = fixed_expenses
        self.fixed_expenses_str = json.dumps(fixed_expenses)