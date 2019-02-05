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

    def add_transaction(self, *, sender, recipient, subject, amount):
        assert amount > 0, 'Amount has to be greater than 0'
        senderexists = False
        recipientexists = False
        for acc in self.accounts:
            if acc['firstname'] == sender['firstname'] and acc['lastname'] == sender['lastname']:
                senderexists = True
                break
        for acc in self.accounts:
            if acc['firstname'] == recipient['firstname'] and acc['lastname'] == recipient['lastname']:
                recipientexists = True
                break

        assert senderexists, 'Sender has no account yet!'
        assert recipientexists, 'Recipient has no account yet!'
        transaction = {'sender': sender, 'recipient': recipient, 'subject': subject, 'amount': amount}
        self.transactions.append(transaction)
        return transaction
