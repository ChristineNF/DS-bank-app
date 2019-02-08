from datetime import datetime


class Transaction:
    def __init__(self, *, sender, recipient, subject, amount, booking_date=datetime.now(), transaction_id=None,
                 category=None):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.amount = amount
        self.booking_date = booking_date
        self.transaction_id = transaction_id
        self.category = category

        assert type(sender) == int, 'Sender needs to be an integer'
        assert type(recipient) == int, 'Recipient needs to be an integer'
        assert type(amount) == float, 'Amount needs to be a float'
        assert amount > 0, 'Amount needs to be greater than 0'

    def info(self):
        return f'From {self.sender} to {self.recipient}: {self.subject} - {self.amount} €'
