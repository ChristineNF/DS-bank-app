import unittest
import app
from datetime import datetime


class TestAccount(unittest.TestCase):
    def test_account_can_be_initialized(self):
        account = app.Account(firstname='Albert',
                              lastname='Einstein',
                              number=1,
                              balance=100.0)
        self.assertTrue(type(account) == app.Account)
        self.assertEqual(account.firstname, 'Albert')
        self.assertEqual(account.lastname, 'Einstein')
        self.assertEqual(account.number, 1)
        self.assertEqual(account.balance, 100.0)

    def test_account_init_number_needs_to_be_an_integer(self):
        message = 'Number needs to be an integer'
        with self.assertRaisesRegex(AssertionError, message):
            app.Account(firstname='Albert',
                        lastname='Einstein',
                        number='1',
                        balance=100.0)

        message = 'Number needs to be an integer'
        with self.assertRaisesRegex(AssertionError, message):
            app.Account(firstname='Albert',
                        lastname='Einstein',
                        number=1.11,
                        balance=100.0)

    def test_account_init_balance_is_optional(self):
        account = app.Account(firstname='Albert',
                              lastname='Einstein',
                              number=1)

        self.assertEqual(account.balance, 0.0)

    def test_account_init_balance_needs_to_be_a_float(self):
        message = 'Balance needs to be a float'
        with self.assertRaisesRegex(AssertionError, message):
            app.Account(firstname='Albert',
                        lastname='Einstein',
                        number=1,
                        balance=100)

        message = 'Balance needs to be a float'
        with self.assertRaisesRegex(AssertionError, message):
            app.Account(firstname='Albert',
                        lastname='Einstein',
                        number=1,
                        balance='100')

    def test_account_info(self):
        account = app.Account(firstname='Albert',
                              lastname='Einstein',
                              number=1,
                              balance=100.0)

        self.assertEqual(account.info(), 'Number 1: Albert Einstein - 100.0 €')

    def test_account_has_funds_for(self):
        account = app.Account(firstname='Albert',
                              lastname='Einstein',
                              number=1,
                              balance=100.0)

        self.assertTrue(account.has_funds_for(10))
        self.assertFalse(account.has_funds_for(500))

    def test_account_has_funds_for_with_zero_balance(self):
        account = app.Account(firstname='Albert',
                              lastname='Einstein',
                              number=1,
                              balance=0.0)

        self.assertFalse(account.has_funds_for(10))

    def test_account_add_to_balance(self):
        account = app.Account(firstname='Albert',
                              lastname='Einstein',
                              number=1,
                              balance=100.0)

        account.add_to_balance(50)

        self.assertEqual(account.balance, 150.0)

    def test_account_add_to_balance_with_zero_or_negative_amount(self):
        account = app.Account(firstname='Albert',
                              lastname='Einstein',
                              number=1,
                              balance=100.0)

        message = 'Amount needs to be greater than 0'
        with self.assertRaisesRegex(AssertionError, message):
            account.add_to_balance(0)

        self.assertEqual(account.balance, 100.0)

        message = 'Amount needs to be greater than 0'
        with self.assertRaisesRegex(AssertionError, message):
            account.add_to_balance(-10)

        self.assertEqual(account.balance, 100.0)

    def test_account_subtract_from_balance(self):
        account = app.Account(firstname='Albert',
                              lastname='Einstein',
                              number=1,
                              balance=100.0)

        account.subtract_from_balance(50)

        self.assertEqual(account.balance, 50.0)

    def test_account_subtract_from_balance_with_not_enough_funds(self):
        account = app.Account(firstname='Albert',
                              lastname='Einstein',
                              number=1,
                              balance=100.0)

        message = 'Account has not enough funds'
        with self.assertRaisesRegex(AssertionError, message):
            account.subtract_from_balance(150)

        self.assertEqual(account.balance, 100.0)

    def test_filter_time_span(self):
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

        transaction1 = bank.add_transaction(sender=anna,
                                            recipient=tom,
                                            subject='Bücher',
                                            amount=100.0,
                                            booking_date=datetime(2017, 7, 30))
        transaction2 = bank.add_transaction(sender=tom,
                                            recipient=anna,
                                            subject='Bücher',
                                            amount=100.0,
                                            booking_date=datetime(2018, 6, 20))
        transaction3 = bank.add_transaction(sender=anna,
                                            recipient=tom,
                                            subject='Bücher',
                                            amount=100.0,
                                            booking_date=datetime(2018, 7, 25))

        message = 'No explicit time span'
        with self.assertRaisesRegex(AssertionError, message):
            anna._filter_time_span(transactions=bank.transactions, startdate=datetime(2018, 1, 1), month=7)

        message = 'No year specified for this month'
        with self.assertRaisesRegex(AssertionError, message):
            anna._filter_time_span(transactions=bank.transactions, month=7)

        selection1 = anna._filter_time_span(transactions=bank.transactions, year=2018)
        self.assertEqual(selection1, [transaction2, transaction3])

        selection2 = anna._filter_time_span(transactions=bank.transactions, year=2018, month=6)
        self.assertEqual(selection2, [transaction2])

        selection3 = anna._filter_time_span(transactions=bank.transactions, startdate=datetime(2017, 8, 5),
                                            enddate=datetime(2018, 7, 20))
        self.assertEqual(selection3, [transaction2])

        selection4 = anna._filter_time_span(transactions=bank.transactions)
        self.assertEqual(selection4, [transaction1, transaction2, transaction3])

    def test_filter_category(self):
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

        transaction1 = bank.add_transaction(sender=anna,
                                            recipient=tom,
                                            subject='Miete',
                                            amount=100.0,
                                            category='Fixkosten',
                                            booking_date=datetime(2017, 7, 30))
        transaction2 = bank.add_transaction(sender=tom,
                                            recipient=anna,
                                            subject='Joghurt',
                                            amount=100.0,
                                            category='Lebensmittel',
                                            booking_date=datetime(2018, 6, 20))
        transaction3 = bank.add_transaction(sender=anna,
                                            recipient=tom,
                                            subject='Bücher',
                                            amount=100.0,
                                            booking_date=datetime(2018, 7, 25))

        selection = anna._filter_category(transactions=bank.transactions, category='Fixkosten')
        self.assertEqual(selection, [transaction1])

    def test_filter_correspondence(self):
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
                                            recipient=anna,
                                            subject='Joghurt',
                                            amount=100.0,
                                            category='Lebensmittel',
                                            booking_date=datetime(2018, 6, 20))
        transaction3 = bank.add_transaction(sender=anna,
                                            recipient=einstein,
                                            subject='Bücher',
                                            amount=100.0,
                                            booking_date=datetime(2018, 7, 25))

        selection = anna._filter_correspondence(transactions=bank.transactions, correspondence=tom.number)
        self.assertEqual(selection, [transaction1, transaction2])

    def _create_transactions(self):
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

        max = bank.open_account(
            app.Account(number=4,
                        firstname='Max',
                        lastname='Mueller',
                        balance=100.0,
                        bank=bank)
        )

        categories = ['Fixkosten', 'Lebensmittel', 'Ausbildung', 'Sport']
        accnames = [anna, tom, einstein, max]

        test_transactions = {}

        for i in range(20):
            pass


    def test_print_statements(self):
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
                                            recipient=anna,
                                            subject='Joghurt',
                                            amount=100.0,
                                            category='Lebensmittel',
                                            booking_date=datetime(2018, 6, 20))
        transaction3 = bank.add_transaction(sender=anna,
                                            recipient=einstein,
                                            subject='Bücher',
                                            amount=100.0,
                                            booking_date=datetime(2018, 7, 25))

        acc_statements = anna.print_statements()
