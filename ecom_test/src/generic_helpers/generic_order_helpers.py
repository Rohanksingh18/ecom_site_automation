from ecom_test.src.dao.order_dao import OrderDAO
from ecom_test.src.dao.products_dao import ProductsDAO
from ecom_test.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper

import json
import os


class GenericOrderHelpers:

    def __init__(self):
        # Initialize instances of helper classes
        self.product_dao = ProductsDAO()  # Helps retrieve product information from the database
        self.order_api_helper = OrdersAPIHelper()  # Assists in making API calls related to orders
        self.cur_file_dir = os.path.dirname(os.path.realpath(__file__))  # Gets the directory path of this script

    def create_order(self, additional_args=None, expected_status_code=201):
        """
        Creates an order with provided or default payload, and returns the API response.

        Args:
        Args:
            additional_args (dict, optional): Additional data to customize the order payload.
            expected_status_code (int, optional): The expected HTTP status code for the API response.

           Coupon: to add coupon add "coupon_lines" field to "additional_args"
            Example: "coupon_lines": [{"code": "<MY COUPON CODE>"}]
        :param product_ids:
        :param customer_id:
        :param coupon_code:
        :param additional_args: Must be a dictionary.
            Example:
                order_payload_addition = {
                                    "line_items": [{"product_id": < some product id >, "quantity": 1}],
                                    "coupon_lines": [{"code": < some coupon code >}],
                                    "shipping_lines": [{"method_id": "flat_rate", "method_title": "Flat Rate", "total": "0.00"}]
                                }

        Returns:
            dict: The API response after creating the order.
        """
        payload_template = os.path.join(self.cur_file_dir, '..', 'data', 'create_order_payload.json')

        # Load the order payload template from a JSON file
        with open(payload_template) as f:
            order_payload = json.load(f)

        # Update payload with additional arguments, if provided
        if additional_args:
            assert isinstance(additional_args,
                              dict), f"Parameter 'additional_args' must be a dictionary but found {type(additional_args)}"
            order_payload.update(additional_args)

        # If no line items are provided, fetch a random product and add it to the order payload
        if additional_args and "line_items" not in additional_args.keys():
            rand_product = self.product_dao.get_random_product_from_db(qty=1)
            rand_product_id = rand_product[0]['ID']
            order_payload["line_items"] = [{"product_id": rand_product_id, "quantity": 1}]

        # If no shipping lines are provided, add default shipping details to the order payload
        if additional_args and "shipping_lines" not in additional_args.keys():
            order_payload["shipping_lines"] = [{"method_id": "flat_rate", "method_title": "Flat Rate", "total": "0.00"}]

        # Make an API call to create the order using the updated payload
        rs_api = self.order_api_helper.call_create_order(payload=order_payload,
                                                         expected_status_code=expected_status_code)

        return rs_api

    @staticmethod
    def verify_order_is_created(order_json, exp_cust_id, exp_products):
        """
        Verifies whether an order has been created successfully based on the provided order JSON response.

        Args:
            order_json (dict): The JSON response received after creating an order.
            exp_cust_id (int): The expected customer ID for the order.
            exp_products (list): List of expected products in the order.

        Raises:
            AssertionError: If any verification step fails.
        """
        orders_dao = OrderDAO()  # Helps retrieve order information from the database

        # Verify the response details
        assert order_json, f"Create order response is empty."
        assert order_json[
                   'customer_id'] == exp_cust_id, f"Create order returned bad customer id. Expected: {exp_cust_id}, Actual: {order_json['customer_id']}"

        # Compare the number of line items in the order with the expected count
        assert len(order_json['line_items']) == len(exp_products), f"Expected {len(exp_products)} \
                                                                   items in order but found {len(order_json['line_items'])}"

        # Verify order details in the database
        order_id = order_json['id']
        line_info = orders_dao.get_order_lines_by_order_id(order_id)
        assert line_info, f"Line item not found in the database for order id: {order_id}"

        # Further verification steps for line items and product IDs
        order_id = order_json['id']
        line_items_db = [item for item in line_info if item['order_item_type'] == 'line_item']
        assert len(
            line_items_db) == 1, f"Expected 1 line item in the database but found {len(line_items_db)}. Order ID: {order_id}"

        # Retrieve the product IDs present in the API response
        api_product_ids = [item['product_id'] for item in order_json['line_items']]

        # Verify that each expected product is included in the order response
        for product in exp_products:
            assert product[
                       'product_id'] in api_product_ids, f"Expected product {product['product_id']} \
                        not found in the order. Order ID: {order_id}"
