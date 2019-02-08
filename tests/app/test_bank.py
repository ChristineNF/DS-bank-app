import unittest
import app
from datetime import datetime


class TestBank(unittest.TestCase):
    def test_bank_can_be_initialized(self):
        bank = app.Bank('GLS')
        self.assertTrue(type(bank) == app.Bank)
        self.assertEqual(bank.name, 'GLS')
        self.assertEqual(bank.accounts, {})
        self.assertEqual(bank.transactions, [])

    def test_open_account(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.accounts, {})

        # Add an account
        account = app.Account(number=1,
                              firstname='Albert',
                              lastname='Einstein')

        bank.open_account(account)

        self.assertEqual(len(bank.accounts), 1)
        self.assertEqual(bank.accounts[1], account)

    def test_open_account_account_needs_to_be_app_account(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.accounts, {})

        # Add an account
        account = {
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
        }

        message = 'Account should be an app.Account'
        with self.assertRaisesRegex(AssertionError, message):
            bank.open_account(account)

        # No account entry saved
        self.assertEqual(bank.accounts, {})

    def test_open_account_number_needs_to_be_unique(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.accounts, {})

        # Add an account
        account = app.Account(number=1,
                              firstname='Albert',
                              lastname='Einstein')
        bank.open_account(account)

        message = 'Account number 1 already taken!'
        with self.assertRaisesRegex(AssertionError, message):
            bank.open_account(account)

        # Only one account entry is saved in accounts
        self.assertEqual(len(bank.accounts), 1)

    def test_open_account_should_return_account(self):
        bank = app.Bank('GLS')

        # Add an account
        account = app.Account(number=1,
                              firstname='Albert',
                              lastname='Einstein')
        einstein = bank.open_account(account)

        self.assertEqual(einstein, account)

    def test_add_transaction(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account(
            app.Account(number=1,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=500.0)
        )
        ehrenfest = bank.open_account(
            app.Account(number=2,
                        firstname='Paul',
                        lastname='Ehrenfest')
        )

        transaction = bank.add_transaction(sender=einstein,
                                           recipient=ehrenfest,
                                           subject='Bücher',
                                           amount=100.0)

        self.assertEqual(len(bank.transactions), 1)
        self.assertEqual(bank.transactions, [transaction])

    def test_add_transaction_with_zero_or_negative_amount(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account(
            app.Account(number=1,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=500.0)
        )
        ehrenfest = bank.open_account(
            app.Account(number=2,
                        firstname='Paul',
                        lastname='Ehrenfest')
        )

        message = 'Amount needs to be greater than 0'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=einstein,
                                 recipient=ehrenfest,
                                 subject='Bücher',
                                 amount=0.0)

        message = 'Amount needs to be greater than 0'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=einstein,
                                 recipient=ehrenfest,
                                 subject='Bücher',
                                 amount=-100.0)

        # No transaction is saved
        self.assertEqual(bank.transactions, [])

    def test_add_transaction_with_invalid_sender(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        # Just the account
        einstein = app.Account(**{
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
            'balance': 500.0
        })

        # Add account
        ehrenfest = bank.open_account(
            app.Account(**{
                'number': 2,
                'firstname': 'Paul',
                'lastname': 'Ehrenfest',
            })
        )

        message = 'Sender has no account yet!'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=einstein,
                                 recipient=ehrenfest,
                                 subject='Bücher',
                                 amount=100.0)

    def test_add_transaction_with_invalid_recipient(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        # Add account
        einstein = bank.open_account(
            app.Account(**{
                'number': 1,
                'firstname': 'Albert',
                'lastname': 'Einstein',
                'balance': 500.0
            })
        )

        # Just the account
        ehrenfest = app.Account(**{
            'number': 2,
            'firstname': 'Paul',
            'lastname': 'Ehrenfest',
        })

        message = 'Recipient has no account yet!'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=einstein,
                                 recipient=ehrenfest,
                                 subject='Bücher',
                                 amount=100.0)

    # Extra Task
    def test_add_transaction_changes_sender_balance(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account(
            app.Account(number=1,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=500.0)
        )
        ehrenfest = bank.open_account(
            app.Account(number=2,
                        firstname='Paul',
                        lastname='Ehrenfest')
        )

        transaction = bank.add_transaction(sender=einstein,
                                           recipient=ehrenfest,
                                           subject='Bücher',
                                           amount=100.0)

        self.assertEqual(einstein.balance, 400.0)
        self.assertEqual(len(bank.transactions), 1)
        self.assertEqual(bank.transactions, [transaction])

    def test_add_transaction_changes_recipient_balance(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account(
            app.Account(number=1,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=500.0)
        )
        ehrenfest = bank.open_account(
            app.Account(number=2,
                        firstname='Paul',
                        lastname='Ehrenfest')
        )

        transaction = bank.add_transaction(sender=einstein,
                                           recipient=ehrenfest,
                                           subject='Bücher',
                                           amount=100.0)

        self.assertEqual(ehrenfest.balance, 100.0)
        self.assertEqual(len(bank.transactions), 1)
        self.assertEqual(bank.transactions, [transaction])

    def test_add_transaction_with_insufficient_funds(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account(
            app.Account(number=1,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=50.0)
        )
        ehrenfest = bank.open_account(
            app.Account(number=2,
                        firstname='Paul',
                        lastname='Ehrenfest')
        )

        message = 'Account has not enough funds'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=einstein,
                                 recipient=ehrenfest,
                                 subject='Bücher',
                                 amount=100.0)

        self.assertEqual(einstein.balance, 50.0)
        self.assertEqual(ehrenfest.balance, 0.0)
        self.assertEqual(bank.transactions, [])

    def test_transactions_for(self):
        bank = app.Bank('GLS')
        anna = bank.open_account(
            app.Account(number=1,
                        firstname='Anna',
                        lastname='Meier',
                        balance=700.0,
                        bank=bank)
        )

        tom = bank.open_account(
            app.Account(number=2,
                        firstname='tom',
                        lastname='Mayer',
                        balance=200.0,
                        bank=bank)
        )

        einstein = bank.open_account(
            app.Account(number=3,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=500.0,
                        bank=bank)
        )

        transaction1 = bank.add_transaction(sender=anna,
                                            recipient=tom,
                                            subject='Miete',
                                            amount=100.0,
                                            category='Fixkosten',
                                            booking_date=datetime(2017, 7, 30))
        transaction2 = bank.add_transaction(sender=tom,
                                            recipient=einstein,
                                            subject='Joghurt',
                                            amount=100.0,
                                            category='Lebensmittel',
                                            booking_date=datetime(2018, 6, 20))
        transaction3 = bank.add_transaction(sender=einstein,
                                            recipient=anna,
                                            subject='Bücher',
                                            amount=100.0,
                                            booking_date=datetime(2018, 7, 25))

        transactions = bank.transactions_for(anna)
        self.assertEqual(transactions, [transaction1, transaction3])
