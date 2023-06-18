
from selenium.webdriver.common.by import By


class HeaderLocators:

    CART_RIGHT_HEADER = (By.CSS_SELECTOR, "a[title='View your shopping cart']") # on the home page right above
    CART_ITEM_COUNT = (By.XPATH, "//span[normalize-space()='1 item']")
    MENU_ITEMS = (By.CSS_SELECTOR, 'div.menu ul.nav-menu li')
