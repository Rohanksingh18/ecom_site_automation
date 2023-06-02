import pytest
from Ecom_test.src.api_helpers.CustomersApiHelpers import CustomersAPIHelper


@pytest.mark.customers
@pytest.mark.tcid33
def test_get_all_customers():
    customers_helper = CustomersAPIHelper()

    # Send GET request to retrieve all customers.
    rs_api = customers_helper.call_list_customers()

    # Verify at least one customer is returned.
    assert rs_api, f"response lsit of all customers is empty"