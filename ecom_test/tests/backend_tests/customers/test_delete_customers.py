from ecom_test.src.api_helpers.CustomersApiHelpers import CustomersAPIHelper
import pytest
import logging as logger
from ecom_test.src.generic_helpers.generic_customer_helpers import GenericCustomerHelpers


# define a function to get customers id
@pytest.fixture(scope='function')
def create_customer():
    customers_helper = CustomersAPIHelper()
    rs_api = customers_helper.call_create_customer()
    assert rs_api, f"response of all list all the customers is empty"
    customer_id = rs_api['id']
    return {'customer_id': customer_id, 'customer_helper': customers_helper}


# Test case: Send DELETE request to delete customer with force=True flag.
@pytest.mark.customers
@pytest.mark.tcid40
# define a subclass to delete customer with a force flag.
def test_delete_customer_with_force_flag(create_customer):

    logger.info("Running test: Verify deleting existing customer with force=True flag works")
    customer_id = create_customer['customer_id']
    customer_helper = create_customer['customer_helper']

    # Send DELETE request to delete customer with force=True flag
    params = {"force": True}
    rs_delete = customer_helper.call_delete_customer(customer_id, params=params)
    # verify
    assert rs_delete['id'] == customer_id, f"delete customer api response has wrong id." \
                                           f"expected: {customer_id}. Actual:{rs_delete['id']}"

    # Call GET /customers and verify customer does not exist
    rs_get = customer_helper.call_get_customer(customer_id, expected_status_code=404)

    # Verify the response attributes after attempting to delete a customer with force=True flag.
    assert rs_get[
               'code'] == 'woocommerce_rest_invalid_id', f"After deleting a customer, the get customer call response has bad 'code request'." \
                                                         f"Expected: 'woocommerce_rest_invalid_id', Actual: '{rs_get['code']}'"
    assert rs_get[
               'message'] == 'Invalid resource ID.', f"After deleting a customer, the get customer call response has bad 'message response'." \
                                                     f"Expected: 'Invalid resource ID.', Actual: '{rs_get['message']}'"
    assert rs_get['data'][
               'status'] == 404, f"After dleting a customer, the get customer call response has bad 'status code'." \
                                 f"Expected: 404, Actual: '{rs_get['data']['status']}'"


# Test case:Verify deleting existing customers without 'force' flag fails.
@pytest.mark.coustomers
@pytest.mark.tcid41
def test_delete_customer_without_force(create_customer):
    logger.info("Running test: Verify deleting existing customer with force=False flag fails")
    customer_id = create_customer['customer_id']
    customer_helper = create_customer['customer_helper']
    # Send DELETE request to delete customer with force=False flag.
    rs_delete = customer_helper.call_delete_customer(customer_id, params={'force': False}, expected_status_code=501)
    # Verify the response attributes after attempting to delete a customer without force=True flag.
    assert rs_delete['code'] == 'woocommerce_rest_trash_not_supported', f"Delete customer without force=True, response has bad 'code'"\
                                                                        f"Expected: 'woocommerce_rest_trash_not_supported' Actual: '{rs_delete['code']}'"

    assert rs_delete['message'] == 'Customers do not support trashing.', f"Delete customer without 'force' flag, response has bad 'message'."\
                                                                         f"Expected: 'Customers do not support trashing.', Actual: '{rs_delete['message']}'"

    assert rs_delete['data']['status'] == 501, f"Delete customer without 'force' flag, response has bad 'status code'."\
                                               f"Expected: 501, Actual: '{rs_delete['data']['status']}'"


# Test case: Verify deleting non-existing customer responds with a correct message.
@pytest.mark.customers
@pytest.mark.tcid42
def test_delete_a_none_existing_customer(create_customer):
    """
    Test case: Verify that deleting a non-existing customer responds with the correct message.

    Alternate test case name:
        Verify deleting a non-existing customer responds with the correct message.

    Steps:
    1. Retrieve the maximum customer ID.
    2. Generate a non-existing customer ID by adding 100 to the maximum ID.
       - To get a customer that does not exist, we get the maximum customer ID
         and make the call for an ID bigger than that.
       - Since customers might be created by other methods, it's not a good idea to just increase the max ID by 1.
       - To be safe, let's increase it by 100 or more. Even 100 can be small, for example, if a load test is running.
    3. Make the DELETE call with the non-existing customer ID.
    4. Verify the response attributes.

    Expected behavior:
    - The response should have the code 'woocommerce_rest_invalid_id'.
    - The response should have the message 'Invalid resource id'.
    - The response status code should be 400.
    """
    logger.info("Running test: Verify deleting non-existing customer responds with correct message")
    # Get the maximum customer ID and generate a non-existing customer ID
    generic_cust_helper = GenericCustomerHelpers()
    max_cust_id = generic_cust_helper.get_max_customer_id()
    none_existing_cust_id = max_cust_id + 100

    # Make the DELETE call and verify the response attributes.
    customers_api_helper = CustomersAPIHelper()
    params = {'force': True}
    rs_delete = customers_api_helper.call_delete_customer(customer_id=none_existing_cust_id, params=params, expected_status_code=400)

    # The response should have the code 'woocommerce_rest_invalid_id'.
    assert rs_delete['code'] == 'woocommerce_rest_invalid_id', f"Delete customer with non-existing customer ID responded with an unexpected 'code'." \
                                                               f" Expected: 'woocommerce_rest_invalid_id', Actual: '{rs_delete['code']}'"
    # The response should have the message 'Invalid resource id'.
    assert rs_delete['message'] == 'Invalid resource id.', f"Delete customer with non-existing customer ID responded with an unexpected 'message'." \
                                                           f" Expected: 'Invalid resource id.', Actual: '{rs_delete['message']}'"
    # The response status code should be 400.
    assert rs_delete['data']['status'] == 400, f"Delete customer with none existing customer id responded with bad 'status code'." \
                                               f"Expected: 400, Actual: '{rs_delete['data']['status']}'"




