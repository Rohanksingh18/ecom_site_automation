from ecom_test.src.utilities.wooAPIUtility import WooAPIUtility
import pytest


# These markers can be used to selectively run or exclude tests based on their assigned markers.
pytestmark = [pytest.mark.products, pytest.mark.smoke]


@pytest.mark.tcid23
def test_get_products_not_empty():
    """
    Verify that the API call 'GET /products' does not return an empty response.
    Ensure that the API, when called to retrieve products, successfully returns a list of products,
    and the response should not be empty.
    """
    # Step 1: Prepare the test environment and dependencies
    woo_api_helper = WooAPIUtility()

    # Step 2: Execute the API call to retrieve all products
    rs_api = woo_api_helper.get(woo_endpoint='products', expected_status_code=200)

    # Step 3: Verify the response data
    assert rs_api, f"API response is empty"


@pytest.mark.tcid24
def test_get_all_products():
    """
    Verify that the API call 'products/id' returns a product with the given id.
    This test ensures that the system can successfully retrieve a product from
    the database by its unique identifier.
    """
    # Step 1: Prepare the test environment and dependencies
    woo_api_helper = WooAPIUtility()

    # Step 2: Execute the API call to retrieve all products
    rs_api = woo_api_helper.get(woo_endpoint='products')

    # Step 3: Verify the response data
    assert rs_api, f"Products not found in the API response"




