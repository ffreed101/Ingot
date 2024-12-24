class Transaction:
    def __init__(self, user_id, date, category, amount, note=""):
        self.user_id = user_id
        self.date = date
        self.category = category
        self.amount = amount
        self.note = note
