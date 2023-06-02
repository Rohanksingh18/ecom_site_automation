
from Ecom_test.src.api_helpers.CustomersApiHelpers import CustomersAPIHelper
import pytest
import logging as logger

# define a function to get customers id

@pytest.fixture(scope='function')
def create_customer():
    customers_helper = CustomersAPIHelper()
    rs_api = customers_helper.call_create_customer()
    assert rs_api, f"response of all list all the customers is empty"
    customer_id = rs_api['id']
    return {'customer_id': customer_id, 'customer_helper':customers_helper}

# Send DELETE request to delete customer with force=True flag
@pytest.mark.customers
@pytest.mark.tcid40

# define a subclass to delete customer with force flag
def test_delete_customer_with_force_flag(create_customer):
    customer_id = create_customer['customer_id']
    customer_helper = create_customer['customer_helper']

    # Send DELETE request to delete customer with force=True flag
    params = {"force": True}
    rs_delete = customer_helper.call_delete_customer(customer_id,params=params)
    # debug
    assert rs_delete['id'] == customer_id, f"delete customer api response has wrong id." \
                                           f"expected: {customer_id}. Actual:{rs_delete['id']}"


    # Call GET /customers and verify customer does not exist
    rs_get = customer_helper.call_get_customer(customer_id, expected_status_code=404)
    assert rs_get['code'] == 'woocommerce_rest_invalid_id', f"After deleting a customer, the get customer call response has bad 'code request'." \
                                                         f"Expected: 'woocommerce_rest_invalid_id', Actual: '{rs_get['code']}'"
    assert rs_get['message'] == 'Invalid resource ID.', f"After deleting a customer, the get customer call response has bad 'message response'." \
                                                     f"Expected: 'Invalid resource ID.', Actual: '{rs_get['message']}'"
    assert rs_get['data'][ 'status'] == 404, f"After dleting a customer, the get customer call response has bad 'status code'." \
                                 f"Expected: 404, Actual: '{rs_get['data']['status']}'"