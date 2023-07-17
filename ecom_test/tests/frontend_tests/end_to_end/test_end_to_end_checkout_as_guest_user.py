import pytest
import logging as logger
from ecom_test.src.pages.HomePage import HomePage
from ecom_test.src.pages.CartPage import CartPage
from ecom_test.src.pages.CheckoutPage import CheckoutPage
from ecom_test.src.pages.Header import Header
from ecom_test.src.pages.OrderReceivedpage import OrderReceivedPage
from ecom_test.src.dao.order_dao import OrderDAO
from ecom_test.src.config.MainConfigs import MainConfigs


@pytest.mark.usefixtures('init_driver')
class TestEndToEndCheckoutGuestUser:
    @pytest.mark.tcid3
    def test_end_to_end_checkout_guest_user(self):
        # getting details from other helper pages
        home_page = HomePage(self.driver)
        header = Header(self.driver)
        cart_page = CartPage(self.driver)
        checkout_page = CheckoutPage(self.driver)
        order_received_page = OrderReceivedPage(self.driver)

        # go to the home page
        home_page.go_to_the_home_page()
        # add an item to the cart
        home_page.click_add_to_cart_btn()
        # wait for page reloading to update the cart
        header.wait_until_cart_item_count(1)
        # now go to the cart page
        header.click_on_cart_on_right_header()
        product_name = cart_page.get_all_product_names_in_cart()
        assert len(
            product_name) == 1, f" 1 product expected but result is {len(product_name)}"  # verifying by assertion

        # apply 100 % free coupon for free checkout
        coupon_code = MainConfigs.get_coupon_code('OFF')
        cart_page.apply_coupon(coupon_code)
        # click on the checkout button
        cart_page.click_on_proceed_to_checkout()
        # fill the user information
        checkout_page.fill_in_billing_info()
        # click on place order button
        checkout_page.click_place_order()
        # now verify order is received
        order_received_page.verify_order_received_page_loaded()
        # verify the database for records (API call)
        order_no = order_received_page.get_order_number()
        logger.info(order_no)
        db_order = OrderDAO().get_order_lines_by_order_id(order_no)
        assert db_order, f" created order not found in db." \
                         f"order_no: {order_no}"
