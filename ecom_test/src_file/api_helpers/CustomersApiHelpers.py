

from ecom_test.src_file.utilities.generic_utilities import generate_random_email_and_password
from ecom_test.src_file.utilities.wooAPIUtility import WooAPIUtility
import logging as logger



class CustomersAPIHelper:

    def __init__(self):
        self.woo_api_utility = WooAPIUtility()

    def call_create_customer(self, email=None, password=None, expected_status_code=201, **kwargs):

        if not email:
            ep = generate_random_email_and_password()
            email = ep['email']
        if not password:
            password = 'Password1'

        payload = dict()
        payload['email'] = email
        payload['password'] = password
        payload.update(kwargs)

        create_user_json = self.woo_api_utility.post('customers', params=payload, expected_status_code=expected_status_code)

        return create_user_json

    def call_list_customers(self, payload=None):

        # if max number of customers per page is not provided then use the max to reduce number of calls
        if not payload:
            payload = {'per_page': 100}
        elif 'per_page' not in payload.keys():
            payload['per_page'] = 100

        rs_api = self.woo_api_utility.get('customers', params=payload, return_headers=True)
        total_number_of_pages = rs_api['headers']['X-WP-TotalPages']

        all_customers = []
        all_customers.extend(rs_api['response_json']) # since the first page is fetched use that
        for i in range(2, int(total_number_of_pages) + 1):  # start from 2 because this will be used for page number and page 1 is fetched already
            logger.debug(f"List Customers page number: {i}")
            payload['page'] = i
            rs_api = self.woo_api_utility.get('customers', params=payload, return_headers=True)
            all_customers.extend(rs_api['response_json'])

        return all_customers

    def call_delete_customer(self, customer_id, params=None, expected_status_code=200):

        rs_api = self.woo_api_utility.delete(f'customers/{customer_id}', params=params, expected_status_code=expected_status_code)

        return rs_api

    def call_get_customer(self, customer_id, expected_status_code=200):

        return self.woo_api_utility

    def call_get_customer(self, customer_id, expected_status_code=200):

        return self.woo_api_utility.get(f'customers/{customer_id}', expected_status_code=expected_status_code)

