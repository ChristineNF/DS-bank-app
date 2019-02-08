import app
from datetime import datetime
from operator import attrgetter


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.transactions = []
        self.transaction_id = 0

    def open_account(self, account):
        if type(account) == app.Account:
            assert account.number not in self.accounts, 'Account number 1 already taken!'
            self.accounts.update({account.number: account})
        else:
            raise AssertionError('Account should be an app.Account')
        return account

    def add_transaction(self, *, sender, recipient, subject, amount, booking_date=None, category=None):
        assert sender.number in self.accounts, 'Sender has no account yet!'
        assert recipient.number in self.accounts, 'Recipient has no account yet!'
        assert amount <= sender.balance, 'Account has not enough funds'
        self.transaction_id += 1
        transaction = app.Transaction(sender=sender.number, recipient=recipient.number, subject=subject, amount=amount,
                                      booking_date=booking_date, category=category, transaction_id=self.transaction_id)
        self.transactions.append(transaction)
        sender.subtract_from_balance(amount)
        recipient.add_to_balance(amount)
        return transaction

    def transactions_for(self, account):
        transact_selection = [tr for tr in self.transactions
                              if (tr.sender == account.number or tr.recipient == account.number)]

        return transact_selection
