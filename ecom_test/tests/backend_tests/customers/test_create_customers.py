import pytest
import logging as logger
from ecom_test.src.utilities.generic_utilities import generate_random_email_and_password
from ecom_test.src.api_helpers.CustomersApiHelpers import CustomersAPIHelper
from ecom_test.src.dao.customers_dao import CustomersDAO
from ecom_test.src.utilities.wooAPIUtility import WooAPIUtility


# define username and password
@pytest.fixture(scope='function')
def create_user_email_password_only():
    rand_info = generate_random_email_and_password()

    email = rand_info['email']
    password = rand_info['password']

    # make the call
    cust_obj = CustomersAPIHelper()
    cust_api_info = cust_obj.call_create_customer(email=email, password=password)

    data = {"email": email, "password": password, "api_response": cust_api_info}

    return data


# Test case: Verify 'POST /customers' creates user with email and password only (tcid20).
@pytest.mark.customers
@pytest.mark.tcid20
def test_create_with_user_email_password_only():
    logger.info("Test: creating a new customer with email and password only.")

    # generate random email and password to register
    rand_info = generate_random_email_and_password()
    email = rand_info['email']
    password = rand_info['password']

    # make an API call
    cust_obj = CustomersAPIHelper()
    cust_api_info = cust_obj.call_create_customer(email=email, password=password)
    # verify the email and first name in the response by validating, first_name used to verify, and it should be empty.
    assert cust_api_info['email'] == email, f"created customer API response returned wrong email. Email: {email}"
    assert cust_api_info['first_name'] == '', f"created customer API response returned value of first_name" \
                                              f"but it should be empty"

    # Now verify, created customer is in database by verifying customer id..
    cust_dao = CustomersDAO()
    cust_info = cust_dao.get_customer_by_email(email)
    id_in_api = cust_api_info['id']  # Response from API
    id_in_db = cust_info[0]['ID']  # id in the DB
    assert id_in_api == id_in_db, f"created customer 'id' does not match with 'ID' in DB." \
                                  f"Email: {email}"


# Test case: Verify 'create customer' fails if email exists (tcid21).
@pytest.mark.customers
@pytest.mark.tcid21
def test_create_customer_fails_for_existing_email():
    # retrieve an existing email from data base.
    cust_dao = CustomersDAO()
    existing_cust = cust_dao.get_random_customer_from_db()
    existing_email = existing_cust[0]['user_email']
    cust_obj = CustomersAPIHelper()
    cust_api_info = cust_obj.call_create_customer(email=existing_email, password="Pass1234", expected_status_code=400)

    # verify for a correct error message
    assert cust_api_info['code'] == 'registration-error-email-exists', f"Created customer with existing user\
                                                                       has wrong error 'code'"\
                                                                       f"Expected error:\
                                                                       'registration-error-email-exists',"\
                                                                       f"Actual: {cust_api_info['code']}"
    assert cust_api_info['message'] == 'An account is already registered with your email address.\
                                       <a href="#" class="showlogin">Please log in.</a>', \
                                       f"Create customer with existing user error 'message' is not correct. " \
                                       f"Expected error: 'An account is already\
                                       registered with your email address. Please log in.', " \
                                       f"Actual error: '{cust_api_info['message']}'"


# Test case: Verify 'POST /customers' fails if password not provided (tcid22).
@pytest.mark.customers
@pytest.mark.tcid22
def test_create_customer_fail_if_password_not_provided():
    # generate random email and password to create a new customer.
    rand_info = generate_random_email_and_password()
    email = rand_info['email']
    # create payload for POST request.
    payload = {'email': email}
    woo_api_utility = WooAPIUtility() # to use woocommerce API
    response_json = woo_api_utility.post('customers', params=payload, expected_status_code=400)
    expected_response = {'code': 'rest_missing_callback_param', 'message': 'Missing parameter(s): password', 'data': {'status': 400, 'params': ['password']}}  # from manual
    # verify by comparing the responses.
    assert response_json == expected_response, f"Got unexpected error creating user without password." \
                                               f"Expected response: {expected_response}." \
                                               f"Actual response: {response_json}"


@pytest.mark.customers
@pytest.mark.tcid31
def test_create_customer_names_should_be_empty_string_if_not_provided():
    """
    Test case: Verify create customer with only email and password provided has
    the names/(first name and last name) of the customer will be empty strings in the system.
    """
    logger.info("TEST: Verify create customer with only email and password has names as empty string")

    # generate email and password
    rand_info = generate_random_email_and_password()
    email = rand_info['email']
    password = rand_info['password']

    # make the call (request to create customer)
    cust_obj = CustomersAPIHelper()
    cust_api_info = cust_obj.call_create_customer(email=email, password=password)

    # Verify names are empty strings
    assert cust_api_info[
               'first_name'] == '', f"Creating user without providing name expected to create first_name=''\
               but it was first_name={cust_api_info['first_name']}"
    assert cust_api_info[
               'last_name'] == '', f"Creating user without providing name expected to create last_name=''\
                but it was first_name={cust_api_info['last_name']}"


# Test case: Verify 'username' is autogenerated based on email.
@pytest.mark.customers
@pytest.mark.tcid32
def test_create_customer_fail_when_no_password_is_provided(create_user_email_password_only):
    logger.info("TEST: Verify 'username' is autogenerated based on email")

    # API call (request)
    api_username = create_user_email_password_only['api_response']['username']
    email = create_user_email_password_only['email']
    expected_username = email.split('@')[0]
    assert api_username == expected_username, f"Creating user with only email and password\
                                              should've created user name based on email." \
                                              f"Expected username: {expected_username}, Actual username: {api_username}"
