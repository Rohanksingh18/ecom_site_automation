
from selenium.webdriver.common.by import By


# To verify logOut button is visible after registration
class MyAccountSignedInPageLocator:
    LEFT_NAV_LOGOUT_BTN = (By.XPATH, "//a[normalize-space()='Logout']")