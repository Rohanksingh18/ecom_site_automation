import pytest
from ecom_test.src.generic_helpers.generic_product_helper import GenericProductHelper
from ecom_test.src.generic_helpers.generic_product_review_helper import GenericProductReviewsHelper
from ecom_test.src.utilities.generic_utilities import generate_random_string, generate_random_email_and_password
import logging as logger


@pytest.fixture(scope="function")
def setup_teardown(request):
    # Create instances of the necessary helper classes
    request.cls.product_helper = GenericProductHelper()
    request.cls.product_review_helper = GenericProductReviewsHelper()

    # Create a product and store its ID for reference
    request.cls.product = request.cls.product_helper.create_a_product()
    request.cls.rating_count_before = request.cls.product['rating_count']
    request.cls.product_id = request.cls.product['id']

    yield request.cls.product_helper, request.cls.product_review_helper, request.cls.product_id
    # They become available to the test function that consumes the fixture

    # Perform cleanup by deleting the product created for the test
    logger.info(f"Running teardown. Deleting product id: {request.cls.product_id}")
    request.cls.product_helper.delete_a_product(request.cls.product_id)


@pytest.mark.usefixtures("setup_teardown")
@pytest.mark.smoke
class TestProductsReviewsSmoke(object):
    """
    Test suite for smoke testing product reviews functionality.
    """

    @pytest.mark.status
    @pytest.mark.parametrize("review_status", [
        pytest.param('hold', marks=[pytest.mark.tcid54]),  # Test case ID: 54, review status: hold
        pytest.param('spam', marks=[pytest.mark.tcid55]),  # Test case ID: 55, review status: spam
        pytest.param('unspam', marks=[pytest.mark.tcid56]),  # Test case ID: 56, review status: un-spam
        pytest.param('trash', marks=[pytest.mark.tcid57]),  # Test case ID: 57, review status: trash
        pytest.param('untrash', marks=[pytest.mark.tcid58])  # Test case ID: 58, review status: un-trash
    ])
    def test_verify_create_review_with_different_statuses(self, setup_teardown, review_status, rating=5):
        """
        Test to verify the creation of a review with different statuses.

        Args:
            setup_teardown: Tuple containing the instances and data from the setup fixture.
            review_status (str): Status of the review to be created.
            Possible values: 'hold', 'spam', 'un-spam', 'trash', 'un-trash'.
            rating (int, optional): Rating for the review (default: 5).

        Steps:
        1. Create a new review for the specified product ID with the given rating and status.
        2. Retrieve the created review using the product review helper.
        3. Determine the expected status based on the review status parameter.
        4. Verify that the created review has the expected status.

        Raises:
            AssertionError: If the status of the retrieved review does not match the expected status.
        """

        product_helper, product_review_helper, product_id = setup_teardown

        logger.info("test_verify_create_review_with_different_statuses")

        # Create a review for the specified product ID with the given rating and status
        review = product_review_helper.create_product_review(
            product_id=product_id,
            review="Automation review: " + generate_random_string(length=10),
            reviewer=f"{generate_random_string(length=5)} {generate_random_string(length=6)}",
            reviewer_email=generate_random_email_and_password()['email'],
            rating=rating,
            status=review_status
        )

        # Retrieve the created review from the product review helper
        review_retrieved = product_review_helper.get_product_review(review['id'])

        # Determine the expected status based on the review status parameter
        expected_status = 'hold' if review_status in ('untrash', 'unspam') else review_status

        # Verify that the created review has the expected status
        assert review_retrieved['status'] == expected_status, \
            f"Failed to create review with status = '{expected_status}'."

    @pytest.mark.tcid59
    def test_verify_review_can_not_be_created_with_invalid_status(self):
        """
        Test to verify that a review cannot be created with an invalid status.

        Steps:
        1. Choose an invalid status for the review.
        2. Attempt to create a review with the invalid status.
        3. Capture the response or error message.
        4. Verify that the review is not created.
        5. Validate the error message or response.

        Raises:
            AssertionError: If the response or error message does not match the expected result.
        """

        # Step 1: Choose an invalid status for the review
        invalid_status = generate_random_string(length=5)
        logger.info("test_verify_review_can_not_be_created_with_invalid_status")

        # Step 2: Attempt to create a review with the invalid status
        review = self.product_review_helper.create_product_review(
            product_id=self.product_id,
            review="Automation review: " + generate_random_string(length=15),
            reviewer=f"{generate_random_string(length=5)} {generate_random_string(length=6)}",
            reviewer_email=generate_random_email_and_password()['email'],
            rating=5,
            status=invalid_status,
            expected_status_code=400
        )

        # Step 3: Capture the response or error message
        expected_error_message = {'code': 'rest_invalid_param', 'data': {'details': {
            'status': {'code': 'rest_not_in_enum', 'data': None, 'message': 'status is not one of approved, '
                                                                            'hold, spam, unspam, trash, and untrash.'}},
            'params': {'status': 'status is not one of approved, hold, spam, unspam, trash, and untrash.'},'status':
                400}, 'message': 'Invalid parameter(s): status'
                                  }

        # Step 4: Verify that the review is not created
        assert review['code'] == expected_error_message['code'], \
            "Response code of creating review with invalid 'status' did not match expected."
        assert review['message'] == expected_error_message['message'], \
            "Response message of creating review with invalid 'status' did not match expected."
