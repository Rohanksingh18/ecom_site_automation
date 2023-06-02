import pytest
from ecom_test.src_file.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from ecom_test.src_file.utilities.generic_utilities import generate_random_email_and_password
from ecom_test.src_file.pages.MyAccountSignedIn import MyAccountSignedIn

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.my_account]


# Test to Verify a valid user should be able to register on the My_Account page

@pytest.mark.usefixtures("init_driver")
class TestRegisterNewUser:

    @pytest.mark.tcid2
    def test_register_vaild_user(self):

        # create class objects ( one for new registration and second one fto verify that new yser is register by checking log-out button in signed In page
        my_acct = MyAccountSignedOutPage(self.driver)
        my_acct_sin = MyAccountSignedIn(self.driver)

        # Go to my account page as logged-out user
        my_acct.go_to_my_account()

        #generate the user name and password as random
        rand = generate_random_email_and_password()

        #fill the user name (random email id)
        my_acct.input_register_email(rand['email'])

        #fill the random password to create new user
        my_acct.input_register_password(rand['password'])

        #click on the registration button to create new user
        my_acct.click_register_button()

        #verify the user is registerd by checking log-out button after registration
        my_acct_sin.verify_user_signed_in()









