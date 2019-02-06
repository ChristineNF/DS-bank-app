import app


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.transactions = []

    def open_account(self, account):
        if type(account) == app.Account:
            assert account.number not in self.accounts, 'Account number 1 already taken!'
            self.accounts.update({account.number: account})
        else:
            raise AssertionError('Account should be an app.Account')
        return account

    def add_transaction(self, *, sender, recipient, subject, amount):
        assert sender.number in self.accounts, 'Sender has no account yet!'
        assert recipient.number in self.accounts, 'Recipient has no account yet!'
        assert amount <= sender.balance, 'Account has not enough funds'
        transaction = app.Transaction(sender=sender.number, recipient=recipient.number, subject=subject, amount=amount)
        self.transactions.append(transaction)
        sender.balance -= amount
        recipient.balance += amount
        return transaction
