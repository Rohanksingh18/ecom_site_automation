
from selenium.webdriver.common.by import By


class HomePageLocators:
    ADD_TO_CART_BTN = (By.XPATH, "//a[@aria-label='Add “Album” to your cart']")
    PAGE_HEAD = (By.CSS_SELECTOR, ".woocommerce-products-header__title.page-title")
    PROD_ELEM = (By.CSS_SELECTOR, "ul.products li.product")  # all the product elements on home_page.

