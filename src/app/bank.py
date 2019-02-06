class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []
        self.transactions = []

    def open_account(self, account):
        accountnumber = account['number']

        for acc in self.accounts:
            if acc['number'] == accountnumber:
                raise(AssertionError('Account number 1 already taken!'))

        self.accounts.append(account)
        return account

    def _check_account_existance(self, account):
        for acc in self.accounts:
            if acc['firstname'] == account['firstname'] and acc['lastname'] == account['lastname']:
                return True
        return False

    def add_transaction(self, *, sender, recipient, subject, amount):
        assert amount > 0, 'Amount has to be greater than 0'
        assert self._check_account_existance(sender), 'Sender has no account yet!'
        assert self._check_account_existance(recipient), 'Recipient has no account yet!'

        transaction = {'sender': sender, 'recipient': recipient, 'subject': subject, 'amount': amount}
        self.transactions.append(transaction)
        return transaction
