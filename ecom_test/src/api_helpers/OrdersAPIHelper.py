
from ecom_test.src.utilities.wooAPIUtility import WooAPIUtility
import os


class OrdersAPIHelper:
    """
    This class provides methods to interact with the WooCommerce API for orders.
    It allows creating, updating, and retrieving order information.
    """

    def __init__(self):
        """
        Constructor to initialize the OrdersAPIHelper class.
        """
        self.woo_api_utility = WooAPIUtility()
        self.cur_file_dir = os.path.dirname(os.path.realpath(__file__))  # Gets the directory path of this script

    def call_create_order(self, payload, expected_status_code=201):
        """
        Calls the WooCommerce API to create a new order.

        :param payload: The payload contains order details.
        :param expected_status_code: The expected HTTP status code.
        :return: The API response for the create order request.
        """
        return self.woo_api_utility.post('orders', params=payload, expected_status_code=expected_status_code)

    def call_update_an_order(self, order_id, payload):
        """
        Calls the WooCommerce API to update an existing order.

        :param order_id: The ID of the order to be updated.
        :param payload: The payload containing order update details.
        :return: The API response for the update order request.
        """
        return self.woo_api_utility.put(f'orders/{order_id}', params=payload)

    def call_retrieve_an_order(self, order_id):
        """
        Calls the WooCommerce API to retrieve details of a specific order.

        :param order_id: The ID of the order to be retrieved.
        :return: The API response for the retrieve order request.
        """
        return self.woo_api_utility.get(f"orders/{order_id}")
