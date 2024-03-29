
import pytest
from ecom_test.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage

# These markers can be used to selectively run or exclude tests based on their assigned markers.
pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.my_account]


@pytest.mark.usefixtures("init_driver")
class TestLoginNegative:

    @pytest.mark.tcid1
    def test_login_none_existing_user(self):
        print("Testing None Existing User Login which is not registered")

        # go to the signed out page
        my_acct_page = MyAccountSignedOutPage(self.driver)
        my_acct_page.go_to_my_account()

        # input un-registered login credentials
        my_acct_page.input_login_username("abcdef@gmail.com")
        my_acct_page.input_login_password("abcdefg123")

        # click on the login button
        my_acct_page.click_login_button()

        # verify the correct error message
        expected_err = "Unknown email address. Check again or try your username."
        my_acct_page.wait_until_error_is_displayed(expected_err)  # wait until the page is reloading




