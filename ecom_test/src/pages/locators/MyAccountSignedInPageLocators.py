
from selenium.webdriver.common.by import By


class MyAccountSignedInPageLocator:
    Left_Nav_LogOut_BTN = (By.XPATH, "//a[normalize-space()='Logout']") #to verfiy logOut button is visbile after registration