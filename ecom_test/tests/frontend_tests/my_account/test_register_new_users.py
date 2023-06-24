import pytest
from ecom_test.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from ecom_test.src.utilities.generic_utilities import generate_random_email_and_password
from ecom_test.src.pages.MyAccountSignedIn import MyAccountSignedIn

# These markers can be used to selectively run or exclude tests based on their assigned markers.
pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.my_account]


# Test to Verify a valid user should be able to register on the My_Account page

@pytest.mark.usefixtures("init_driver")
class TestRegisterNewUser:

    @pytest.mark.tcid2
    def test_register_valid_user(self):

        # create class objects (one for new registration, and second one fto verify that new user is register by
        # checking log-out button in signed In page
        my_acct = MyAccountSignedOutPage(self.driver)
        my_acct_sin = MyAccountSignedIn(self.driver)

        # Go to my account page as logged-out user
        my_acct.go_to_my_account()

        # generate the username and password as random
        rand = generate_random_email_and_password()

        # fill the username (random email id)
        my_acct.input_register_email(rand['email'])

        # fill the random password to create a new user
        my_acct.input_register_password(rand['password'])

        # click on the registration button to create a new user
        my_acct.click_register_button()

        # verify the user is registered by checking log-out button after registration
        my_acct_sin.verify_user_signed_in()









