from selenium.webdriver import ActionChains

from Ecom_test.src.selenium_extended.SeleniumExtended import SeleniumExtended
from Ecom_test.src.config.MainConfigs import MainConfigs
from Ecom_test.src.pages.locators.HomePageLocators import HomePageLocators



class HomePage(HomePageLocators):

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def go_to_the_home_page(self):
        homepage_url = MainConfigs.get_base_url()
        self.driver.get(homepage_url)

    def click_add_to_cart_btn(self):
        self.sl.wait_and_click(self.Add_To_Cart_BTN)



