import pytest
from ecom_test.src.generic_helpers.generic_product_helper import GenericProductHelper
from ecom_test.src.generic_helpers.generic_order_helpers import GenericOrderHelpers

pytestmark = [pytest.mark.products, pytest.mark.smoke]


@pytest.fixture()
def setup():
    """
    Test fixture to set up the required environment for the test.
    """
    generic_product_helper = GenericProductHelper()
    generic_order_helper = GenericOrderHelpers()
    random_product = generic_product_helper.get_random_products(qty=1)

    return {
        "generic_product_helper": generic_product_helper,
        "generic_order_helper": generic_order_helper,
        "random_product": random_product
    }


@pytest.mark.parametrize("ordered_qty",
                         [
                             pytest.param(1, marks=[pytest.mark.tcid60]),
                             pytest.param(3, marks=[pytest.mark.tcid61]),
                         ])
def test_product_total_sales_updated(setup, ordered_qty):
    """
    Test case to verify that a product's 'total_sales'
    attribute gets updated correctly when items are ordered.

    Subpart:
    - Ordered quantity: 1 item (tcid60)
    - Ordered quantity: 3 items (tcid61)

    Steps:
    1. Prepare the test environment by setting up generic product and order helpers.
    2. Retrieve a random product using the generic product helper.
    3. Get the initial 'total_sales' value of the product.
    4. Create an order with the specified quantity of the product.
    5. Get the updated product details using the product ID.
    6. Verify that the 'total_sales' attribute is updated correctly based on the ordered quantity.

    Args:
        setup (fixture): The test setup fixture.
        ordered_qty (int): The quantity of items to be ordered.
    """
    # Step 1: Setup
    generic_product_helper = setup["generic_product_helper"]
    generic_order_helper = setup["generic_order_helper"]
    random_product = setup['random_product']
    product_id = random_product[0]['id']
    initial_total_sales = random_product[0]['total_sales']
    # Step 4: Create an order with the specified quantity
    partial_payload = {"line_items": [{"product_id": product_id, "quantity": ordered_qty}]}
    generic_order_helper.create_order(additional_args=partial_payload)

    # Step 5: Get the updated product details
    product_details = generic_product_helper.get_product_detail_via_api(product_id)
    updated_total_sales = product_details['total_sales']

    # Step 6: Verify the 'total_sales' is updated correctly
    expected_total_sales_after = initial_total_sales + ordered_qty
    assert updated_total_sales == expected_total_sales_after, f"The 'total_sales' parameter of a " \
                                                              f"product expected to update " \
                                                              f"after placing an order for the product." \
                                                              f"Actual value: {updated_total_sales}, " \
                                                              f"Expected value: {expected_total_sales_after}"
