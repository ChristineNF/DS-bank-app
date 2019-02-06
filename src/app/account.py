class Account:
    def __init__(self, *, firstname, lastname, number, balance=None):
        self.firstname = firstname
        self.lastname = lastname
        self.number = number
        self.balance = balance

        assert type(self.number) == int, 'Number needs to be an integer'

        if self.balance is not None:
            assert type(self.balance) == float, 'Balance needs to be a float'
        else:
            self.balance = 0.0

    def info(self):
        return f'Number {self.number}: {self.firstname} {self.lastname} - {self.balance} €'

    def has_funds_for(self, amount):
        if amount <= self.balance:
            return True
        else:
            return False

    def add_to_balance(self, amount):
        assert amount > 0, 'Amount needs to be greater than 0'
        self.balance += amount

    def subtract_from_balance(self, amount):
        assert amount <= self.balance, 'Account has not enough funds'
        self.balance -= amount
