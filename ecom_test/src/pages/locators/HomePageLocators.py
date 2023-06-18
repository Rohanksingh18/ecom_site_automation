
from selenium.webdriver.common.by import By


class HomePageLocators:
    Add_To_Cart_BTN = (By.XPATH,"//a[@aria-label='Add “Album” to your cart']")
    Page_heading = (By.CSS_SELECTOR,".woocommerce-products-header__title.page-title")
    Product_Elements = (By.CSS_SELECTOR, "ul.products li.product")  # all the product elements on home_page.

