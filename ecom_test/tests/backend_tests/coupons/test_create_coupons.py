from ecom_test.src.utilities.generic_utilities import generate_random_coupon_code, generate_random_string
from ecom_test.src.api_helpers.CouponsAPIHelper import CouponsAPIHelper
import pytest
import random
from ecom_test.src.utilities.wooAPIUtility import WooAPIUtility


# These markers can be used to selectively run or exclude tests based on their assigned markers.
pytestmark = [pytest.mark.regression, pytest.mark.coupons]


@pytest.fixture(scope='module')
def my_setup():
    """
    This fixture sets up the necessary objects and resources for the tests
    and returns a dictionary containing the CouponsAPIHelper instance.
    The test function includes multiple parametrized test cases using pytest.mark.parametrize.
    Each test case represents a different discount type.
    The pytest.mark.tcid and pytest.mark.smoke marks are used to categorize and label the test cases.
    """
    info = {'coupon_helper': CouponsAPIHelper()}
    return info


@pytest.mark.parametrize("discount_type",
                         [
                             pytest.param(None, marks=[pytest.mark.tcid43, pytest.mark.smoke]),
                             pytest.param('percent', marks=[pytest.mark.tcid44, pytest.mark.smoke]),
                             pytest.param('fixed_product', marks=pytest.mark.tcid45),
                             pytest.param('fixed_cart', marks=pytest.mark.tcid46),
                         ])
def test_create_coupon_percent_discount_type(my_setup, discount_type):
    """
    Create a new coupon with 'discount_type=None'. If None is given, check for default.
    The expected discount type is determined based on the value of the discount_type parameter.
    If discount_type is None, the expected discount type is set to 'fixed_cart'.
    Otherwise, it is set to the value of discount_type.
    """
    expected_discount_type = discount_type if discount_type else 'fixed_cart'

    # The range for the discount is set between 50 and 80, and the value is converted to a string with ".00" appended.
    pct_off = str(random.randint(50, 80)) + ".00"
    # appending "tcid44" as a suffix to make it unique.
    coupon_code = generate_random_coupon_code(suffix="tcid44", length=5)
    # The Object is retrieved from the my_setup fixture, which provides access to the CouponsAPIHelper class.
    coupon_helper = my_setup['coupon_helper']

    # Create payload dictionary and call API.
    pyload = dict()
    pyload['code'] = coupon_code
    pyload['amount'] = pct_off
    if discount_type:
        pyload['discount_type'] = discount_type
    rs_coupon = coupon_helper.call_create_coupon(payload=pyload)
    coupon_id = rs_coupon['id']

    # Verify coupon is created. This method retrieves the coupon details from the API.
    rs_coupon_2 = coupon_helper.call_retrieve_coupon(coupon_id)

    # Verification of the responses.
    assert rs_coupon_2['amount'] == pct_off, f"Create coupon with % off responded {rs_coupon_2['amount']} for amount."\
                                             f"Expected: {pct_off}, Actual: {rs_coupon_2['amount']}."
    assert rs_coupon_2['code'] == coupon_code.lower(), f"Created coupon response has wrong 'code'. "\
                                                       f"Expected: {coupon_code.lower()}, Actual: {rs_coupon_2['code']}."
    assert rs_coupon_2['discount_type'] == expected_discount_type, f"Create coupon responded with wrong 'discount_type'."\
                                                                   f"Expected: {expected_discount_type}, Actual:\
                                                                   {rs_coupon_2['discount_type']}."


@pytest.mark.tcid47
def test_create_coupon_with_invalid_type():
    """
    Test case (tcid47) is to verify that using an invalid value for
    the 'discount_type' parameter during coupon creation
    will result in the correct error message. The payload is assigned a randomly generated string.
    The WooAPIUtility().post() method is called with the 'coupons' endpoint and the prepared payload.
    The expected status code is set to 400 to indicate an error response.
    """
    # Create payload dictionary and call API.
    pyload = dict()
    pyload['code'] = generate_random_coupon_code(suffix='tcid47', length=5)
    # The code is given the suffix "tcid47" and has a length of 5.
    pyload['discount_type'] = generate_random_string()
    rs_coupon = WooAPIUtility().post('coupons', params=pyload, expected_status_code=400)

    # Verification by assertions.
    assert rs_coupon['code'] == 'rest_invalid_param', f"Created coupon with invalid 'discount_type' " \
                                                      f"returned 'code={rs_coupon['code']}',\
                                                      Expected code = 'rest_invalid_param' "
    assert rs_coupon['message'] == 'Invalid parameter(s): discount_type', f"Created coupon with invalid 'discount_type'"\
                                                                          f"returned 'message={rs_coupon['message']}',\
                                                            Expected message = 'Invalid parameter(s): discount_type',"






