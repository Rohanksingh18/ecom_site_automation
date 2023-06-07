
from selenium.webdriver.common.by import By


class HomePageLocators:
    Add_To_Cart_BTN = (By.XPATH,"//a[@aria-label='Add “Album” to your cart']")
    Page_heading = (By.XPATH, "//a[contains(text(),'My_Ecom_Test_Site')]")

