
from ecom_test.src.api_helpers.CustomersApiHelpers import CustomersAPIHelper


class GenericCustomerHelpers:
    def __init__(self):
        self.customer_api_helpers = CustomersAPIHelper()

# Calls list all customers endpoint sorting it by 'id' descending(desc) and gets the id of the first customer
    def get_max_customer_id(self):
        params = {"orderby":'id', "order":'desc'}
        all_customers = self.customer_api_helpers.call_list_customers(payload=params)
        latest_customer = all_customers[0]
        max_customer_id = latest_customer['id']

        return max_customer_id  # Returns the highest customer id available.


