#!/usr/bin/env python3
'''
Creating customer database for Norton Furniture
'''
import logging
import peewee
import customer_schema as cs

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

logging.info('Starting basic operations for customer database.')

# pylint: disable=R0913
def add_customer(customer_id, first_name, last_name, home_address, phone_number,
                 email_address, active_status, credit_limit):
    '''
    Adding a new customer to the DB
    '''
    try:
        new_customer = cs.Customer.create(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            phone_number=phone_number,
            email_address=email_address,
            active_status=active_status,
            credit_limit=credit_limit)
        new_customer.save()
        logging.info('%s %s has been added to the database.', first_name,
                     last_name)
    except peewee.IntegrityError as add_error:
        logging.error('%s. Error cannot add %s %s to the database.', add_error,
                      first_name, last_name)
        raise peewee.IntegrityError


def delete_customer(customer_id):
    '''
    Deleting a customer from the DB
    '''
    try:
        former_customer = cs.Customer.get(cs.Customer.customer_id == customer_id)
        logging.info('%s: %s %s has been removed from the database.', customer_id,
                     former_customer.first_name, former_customer.last_name)
        former_customer.delete_instance()
    except peewee.DoesNotExist:
        logging.error('Non-existant customer.')


def search_customer(customer_id):
    '''
    Search DB for an active customer
    '''
    try:
        current_customer = cs.Customer.get(cs.Customer.customer_id == customer_id)

        customer_dict = {'first_name': current_customer.first_name,
                         'last_name': current_customer.last_name,
                         'email_address': current_customer.email_address,
                         'phone_number': current_customer.phone_number}
        logging.info('%s: %s %s exists', customer_id,
                 current_customer.first_name, current_customer.last_name)

    return customer_dict

except peewee.DoesNotExist:
        logging.error('Non-existant customer.')
        return dict()


def list_active_customers():
    '''
    List all active customers
    '''
    pass

def update_customer_credit():
    '''
    Update customer credit limits
    '''
    pass
