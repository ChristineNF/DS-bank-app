import app
from datetime import datetime
from operator import attrgetter
import calendar


class Account:
    def __init__(self, *, firstname, lastname, number, bank=None, balance=None):
        self.firstname = firstname
        self.lastname = lastname
        self.number = number
        self.bank = bank
        self.balance = balance
        self.start_balance = balance

        assert type(self.number) == int, 'Number needs to be an integer'

        if self.balance is not None:
            assert type(self.balance) == float, 'Balance needs to be a float'
        else:
            self.balance = 0.0

    def info(self):
        return f'Number {self.number}: {self.firstname} {self.lastname} - {self.balance} €'

    def has_funds_for(self, amount):
        return amount <= self.balance

    def add_to_balance(self, amount):
        assert amount > 0, 'Amount needs to be greater than 0'
        self.balance += amount

    def subtract_from_balance(self, amount):
        assert self.has_funds_for(amount), 'Account has not enough funds'
        self.balance -= amount

    @staticmethod
    def _filter_time_span(*, transactions, startdate=None, enddate=None, year=None, month=None):
        assert ((startdate is None and enddate is None) or (year is None and month is None)), 'No explicit time span'
        if month:
            assert year is not None, 'No year specified for this month'

        if year:
            transactions = [tr for tr in transactions if tr.booking_date.year == year]
            if month:
                transactions = [tr for tr in transactions if tr.booking_date.month == month]
        if startdate:
            transactions = [tr for tr in transactions if tr.booking_date >= startdate]
        if enddate:
            transactions = [tr for tr in transactions if tr.booking_date <= enddate]
        return transactions

    @staticmethod
    def _filter_category(transactions, category):
        return [tr for tr in transactions if tr.category == category]

    @staticmethod
    def _filter_correspondence(transactions, correspondence):
        return [tr for tr in transactions if (tr.sender == correspondence or tr.recipient == correspondence)]

    # prints statements in certain period, from certain category or correspondence with certain accounts
    def print_statements(self, *, year=None, month=None, startdate=None, enddate=None, category=None,
                         correspondence=None):
        assert self.bank is not None, 'Account has no bank'
        acc_statements = '{0:<14} {1:>8} {2:>6} {3:>9} {4:<8} {5:<8} {6:>8}\n'.format('TransactionID', 'BookingDate',
                                                                                      'Sender', 'Recipient', 'Subject',
                                                                                      'Category', 'Amount €')
        faccstmt = open('./accountStatement.txt', 'w')
        faccstmt.write(acc_statements)

        transact_selection = self.bank.transactions_for(self)
        faccstmt.write(f'{len(transact_selection)}')
        transact_selection = self._filter_time_span(transactions=transact_selection, startdate=startdate,
                                                    enddate=enddate, year=year, month=month)
        faccstmt.write(f'{len(transact_selection)}')
        transact_selection = self._filter_category(transactions=transact_selection, category=category)
        faccstmt.write(f'{len(transact_selection)}')
        transact_selection = self._filter_correspondence(transactions=transact_selection, correspondence=correspondence)
        faccstmt.write(f'{len(transact_selection)}')
        transact_selection = sorted(transact_selection, key=attrgetter('booking_date'))


        for tr in transact_selection:
            acc_statements += 'bla\n'
        #     acc_statements += '{0:<14} {1:>8} {2:>6} {3:>9} {4:<8} {5:<8} {6:>8}\n'.format(tr.transaction_id,
        #                                                                                  tr.booking_date,
        #                                                                                  tr.sender, tr.recipient,
        #                                                                                  tr.subject, tr.category,
        #                                                                                  self.balance)

        faccstmt.write(f'{len(transact_selection)}')
        faccstmt.close()

        return acc_statements
