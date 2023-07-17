
import pytest
from ecom_test.src.generic_helpers.generic_coupon_helper import GenericCouponHelper
from ecom_test.src.pages.HomePage import HomePage
from ecom_test.src.pages.CartPage import CartPage
from ecom_test.src.pages.Header import Header


# 'init_driver' fixture for setting up the driver
@pytest.mark.usefixtures("init_driver")
class TestCartExpiredCoupon:

    @pytest.fixture(scope='class')
    def setup(self, request):
        """
        Test fixture for setting up the environment for the test case.
        It creates an expired coupon, initializes the necessary page objects,
        and performs cleanup after the test case is executed.

        Args:
            request: pytest request object to access the test context.
        """
        coupon_helper = GenericCouponHelper()

        # Step 1: Create an expired coupon
        expired_coupon = coupon_helper.create_coupon(expired=True)

        # Step 2: Set the 'expired_coupon' attribute in the test class
        request.cls.expired_coupon = expired_coupon

        # Step 3: Initialize the page objects
        request.cls.homepage = HomePage(self.driver)
        request.cls.cart = CartPage(self.driver)
        request.cls.header = Header(self.driver)

        yield

        # Step 5: Delete the expired coupon
        coupon_helper.delete_coupon(coupon_code=expired_coupon)

    @pytest.mark.tcid11
    def test_expired_coupon_message(self, setup):
        """
        Test case to verify that an expired coupon displays the correct error message.

        Args:
            setup: Fixture to set up the test environment.
        """
        # Step 1: Go to the home page
        self.homepage.go_to_the_home_page()

        # Step 2: Click the 'Add to Cart' button for the first item
        self.homepage.click_add_to_cart_btn()

        # Step 3: Wait until the cart item count becomes 1
        self.header.wait_until_cart_item_count(1)

        # Step 4: Go to the cart page
        self.cart.go_to_cart_page()

        # Step 5: Apply the expired coupon to the cart
        self.cart.apply_coupon(self.expired_coupon, expect_success=False)

        # Step 6: Get the displayed error message
        err_msg = self.cart.get_displayed_error()

        # Step 7: Verify that the error message is 'This coupon has expired (Taken from ecom-website)'
        assert err_msg == 'This coupon has expired.', "Expired coupon error-msg not displayed."

