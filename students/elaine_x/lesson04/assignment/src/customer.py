"""
    Learning persistence with Peewee and sqlite
    Add customers from csv
        (but running this program does not require it)


"""

import csv
import logging
from peewee import *
from customer_model import Customer

LOGGER = logging.getLogger()

DATABASE = SqliteDatabase('customer.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


def read_csv(path):
    '''
    read in csv as a list
    '''
    with open(path, 'r') as file:
        readcsv = csv.reader(file, delimiter=',')
        customers = []
        iterator = iter(readcsv)
        while True:
            try:
                row = next(iterator)
                #LOGGER.info(f'print {row}')
                customers.append(row)
            except StopIteration:
                LOGGER.info('Stop Iteration')
                break
            except UnicodeDecodeError as error_message:
                LOGGER.info('Error reading')
                LOGGER.info(error_message)
    return customers


CUSTOMER_ID = 0
CUSTOMER_NAME = 1
CUSTOMER_LASTNAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
STATUS = 6
CREDIT_LIMIT = 7


LOGGER.info('Creating Customer records: iterate through the list of tuples')
LOGGER.info('Prepare to explain any errors with exceptions')
LOGGER.info('and the transaction tells the database to rollback on error')


def customer_iterator(an_iterable):
    """
    Emulation of a for loop.
    func() will be called with each item in an_iterable
    """
    customer_iter = iter(an_iterable)
    while True:
        try:
            customer = next(customer_iter)
            #LOGGER.info(customer)
        except StopIteration:
            break
        add_customer_list(customer)


def add_customer_list(customer):
    '''
    add a new customer to the database
    '''
    try:
        with DATABASE.transaction():
            new_customer = Customer.create(
                customer_id=customer[CUSTOMER_ID],
                customer_name=customer[CUSTOMER_NAME],
                customer_lastname=customer[CUSTOMER_LASTNAME],
                home_address=customer[HOME_ADDRESS],
                phone_number=customer[PHONE_NUMBER],
                email_address=customer[EMAIL_ADDRESS],
                status=customer[STATUS],
                credit_limit=customer[CREDIT_LIMIT]
                )
            new_customer.save()
            LOGGER.info('%s Database add successful', customer[CUSTOMER_ID])

    # it was giving me model based error type,
    # not sure what error type would work here?
    except Exception as error_message:
        LOGGER.info('Error creating = %s', customer[CUSTOMER_ID])
        LOGGER.info(error_message)
        LOGGER.info('See how the database protects our data')


if __name__ == '__main__':
    CUSTOMERS = read_csv('../data/customer.csv')
    customer_iterator(CUSTOMERS)

DATABASE.close()
