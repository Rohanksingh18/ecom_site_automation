
from ecom_test.src.selenium_extended.SeleniumExtended import SeleniumExtended
from ecom_test.src.pages.locators.CartPageLocators import CartPageLocators
from ecom_test.src.config.MainConfigs import MainConfigs


class CartPage(CartPageLocators):

    endpoint = '/cart'

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def go_to_cart_page(self):
        base_url = MainConfigs.get_base_url()
        cart_url = base_url + self.endpoint
        self.driver.get(cart_url)

    def verify_cart_page_url(self):
        self.sl.wait_until_url_contains('/cart/')

    def get_all_product_names_in_cart(self):

        product_name_elements = self.sl.wait_and_get_elements(self.PRODUCT_NAMES_IN_CART)
        product_names = [i.text for i in product_name_elements]
        # import pdb; pdb.set_trace()
        return product_names

    def input_coupon(self, coupon_code):
        self.sl.wait_and_input_text(self.COUPON_FIELD, coupon_code)

    def click_apply_coupon(self):
        self.sl.wait_and_click(self.APPLY_COUPON_BTN)

    def apply_coupon(self, coupon_code, expect_success=True):
        self.input_coupon(coupon_code)
        self.click_apply_coupon()
        if expect_success:
            displayed_notice = self.get_displayed_message()
            assert displayed_notice == 'Coupon code applied successfully.', \
                f"Applied coupon '{coupon_code}' but did not get successful messages."

    def get_displayed_message(self):
        txt = self.sl.wait_and_get_text(self.CART_PAGE_MESSAGE)
        return txt

    def get_displayed_error(self):
        return self.sl.wait_and_get_text(self.ERROR_BOX)

    def click_on_proceed_to_checkout(self):
        self.sl.wait_and_click(self.PROCEED_TO_CHECKOUT_BTN)