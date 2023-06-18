
from selenium.webdriver.common.by import By


class OrderReceivedPageLocators:

    PAGE_MAIN_HEADER = (By.XPATH, "//h1[normalize-space()='Order received']")
    ORDER_NUMBER = (By.CSS_SELECTOR, "li[class='woocommerce-order-overview__order order'] strong")