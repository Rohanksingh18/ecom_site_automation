
from selenium.webdriver.common.by import By


class CartPageLocators:
    PRODUCT_NAMES_IN_CART = (By.XPATH, "//a[contains(text(),'Album')]")
    COUPON_FIELD = (By.ID, 'coupon_code')
    APPLY_COUPON_BTN = (By.XPATH, "//button[contains(text(),'Apply coupon')]")
    CART_PAGE_MESSAGE = (By.XPATH, "//div[@role='alert']" )
    PROCEED_TO_CHECKOUT_BTN = (By.XPATH, "//a[normalize-space()='Proceed to checkout']")
    ERROR_BOX = (By.CSS_SELECTOR, 'div.woocommerce-notices-wrapper ul.woocommerce-error')