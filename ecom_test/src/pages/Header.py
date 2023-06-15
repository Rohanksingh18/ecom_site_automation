from ecom_test.src.selenium_extended.SeleniumExtended import SeleniumExtended
from ecom_test.src.pages.locators.HeaderLocators import HeaderLocators

class Header(HeaderLocators):

    expected_menu_items = ['Home', 'Cart', 'Checkout', 'My account', 'Sample Page']

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def click_on_cart_on_right_header(self):
        self.sl.wait_and_click(self.CART_RIGHT_HEADER)

    def wait_until_cart_item_count(self, count):
        expected_text = str(count) + ' item'
        self.sl.wait_until_element_contains_text(self.CART_ITEM_COUNT, expected_text)

    def get_all_menu_item_text(self):
        elms = self.sl.wait_and_get_elements(self.MENU_ITEMS)
        menu_text = [elm.text for elm in elms]
        return menu_text

    def assert_all_menu_items_displayed(self):
        displayed_menu_items = self.get_all_menu_item_text()
        for menu in self.expected_menu_items:
            if menu not in displayed_menu_items:
                raise Exception(f"Menu item '{menu}' is not displayed in the header.")