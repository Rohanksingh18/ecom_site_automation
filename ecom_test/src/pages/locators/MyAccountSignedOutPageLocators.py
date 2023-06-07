
from selenium.webdriver.common.by import By

class MyAccountSignedOutPageLocators:

    LOGIN_USER_NAME = (By.XPATH, '//*[@id="username"]')
    LOGIN_USER_PASSWORD = (By.XPATH, '//*[@id="password"]')
    LOGIN_BTN = (By.CSS_SELECTOR, '#customer_login > div.u-column1.col-1 > form > p:nth-child(3) > button')

    ERRORS_UL = (By.CSS_SELECTOR, '#content > div > div.woocommerce > ul')

    REGISTER_EMAIL = (By.XPATH, '//*[@id="reg_email"]')
    REGISTER_PASSWORD = (By.XPATH, '//*[@id="reg_password"]')
    REGISTER_BTN = (By.XPATH, " //button[@name='register']")