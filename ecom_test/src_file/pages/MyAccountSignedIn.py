
from ecom_test.src_file.selenium_extended.SeleniumExtended import SeleniumExtended
from ecom_test.src_file.pages.locators.MyAccountSignedInPageLocators import MyAccountSignedInPageLocator


class MyAccountSignedIn(MyAccountSignedInPageLocator):
    def __init__(self, driver):
        self.sl = SeleniumExtended(driver)

    def verify_user_signed_in(self):
        self.sl.wait_until_element_is_visible(self.Left_Nav_LogOut_BTN) # verify user is signed in by checking the logout button is diplaying