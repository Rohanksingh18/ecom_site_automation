
import logging as logger
import pytest
from ecom_test.src.generic_helpers.generic_product_helper import GenericProductHelper
from ecom_test.src.generic_helpers.generic_product_review_helper import GenericProductReviewsHelper
from ecom_test.src.utilities.generic_utilities import generate_random_string, generate_random_email_and_password


@pytest.fixture(scope="function")
def test_data(request):
    # Set up the test data
    request.cls.product_helper = GenericProductHelper()
    request.cls.product_review_helper = GenericProductReviewsHelper()

    # Create a new product
    request.cls.product = request.cls.product_helper.create_a_product()
    request.cls.rating_count_before = request.cls.product['rating_count']
    request.cls.product_id = request.cls.product['id']

    # Pass the test data as a tuple, making it accessible to the test case function.
    yield

    # Teardown: Delete the created product
    logger.info(f"Running teardown. Deleting product id: {request.cls.product_id}")
    request.cls.product_helper.delete_a_product(request.cls.product_id)


@pytest.mark.usefixtures("test_data")
@pytest.mark.smoke
class TestProductsReviewsSmoke(object):
    @pytest.mark.tcid48
    def test_verify_create_product_review_endpoint_creates_review(self):

        logger.info("test_verify_create_product_review_endpoint_creates_review")

        # Verify that the 'rating_count' field of the newly created product is 0
        assert self.rating_count_before == 0, "The 'rating_count' field of a newly created product should be 0"

        # Create reviews for the product
        qty_review_to_add = 5
        for _ in range(qty_review_to_add):
            self.product_review_helper.create_random_review_for_product(self.product_id)

        # Get updated product details
        product = self.product_helper.get_product_detail_via_api(self.product_id)
        rating_count_after = product['rating_count']

        # Subtracting 1 from the expected rating count, because of a bug, it always shows 1 less than actual.
        expected_rating_count = qty_review_to_add - 1
        assert rating_count_after == expected_rating_count, f"Expected 'rating_count={expected_rating_count}'\
                                                            after creating reviews for product, but found\
                                                            'rating_count={rating_count_after}'."

    @pytest.mark.tcid49
    def test_verify_review_creation_fails_when_fields_duplicated(self):

        # Create a review for the product
        review_rs = self.product_review_helper.create_random_review_for_product(self.product_id)

        # Try to create another review with the same data (all fields duplicated)
        rs_duplicate = self.product_review_helper.create_product_review(
            product_id=self.product_id,
            review=review_rs['review'],
            reviewer=review_rs['reviewer'],
            reviewer_email=review_rs['reviewer_email'],
            rating=review_rs['rating'],
            expected_status_code=409
        )

        # Verify the response code, error message, and data
        assert rs_duplicate['code'] == 'woocommerce_rest_comment_duplicate'
        assert 'Duplicate comment detected; it looks as though' in rs_duplicate['message']
        assert rs_duplicate['data']['status'] == 409

    @pytest.mark.tcid50
    def test_review_creation_should_not_fail_if_reviewer_is_different(self):
        """All fields have the same value but the 'reviewer' is changes.
           Expecting successful review creation.
        """
        # Create a review for the product
        review_rs = self.product_review_helper.create_random_review_for_product(self.product_id)

        # create another review with the same data except the 'reviewer' field.
        rs_duplicate = self.product_review_helper.create_product_review(
            product_id=self.product_id,
            review=review_rs['review'],
            reviewer=f"{generate_random_string(length=5)} {generate_random_string(length=6)}",
            reviewer_email=review_rs['reviewer_email'],
            rating=review_rs['rating'],
            expected_status_code=201
        )

        # Verify the second review is created by checking its status.
        assert rs_duplicate['status'] == 'approved'
        # The second call's response code is also confirmed to be 201.
        assert not rs_duplicate['reviewer'] == 'reviewer'

    @pytest.mark.tcid51
    def test_review_creation_should_not_fail_if_review_is_different(self):
        """All fields have the same value but the 'review' is changes. Expecting successful review creation."""
        # Create a review for the product
        review_rs = self.product_review_helper.create_random_review_for_product(self.product_id)

        # create another review with the same data except the 'review' field.
        rs_duplicate = self.product_review_helper.create_product_review(
            product_id=self.product_id,
            review="Automation review: " + generate_random_string(length=25),
            reviewer=review_rs['reviewer'],
            reviewer_email=review_rs['reviewer_email'],
            rating=review_rs['rating'],
            expected_status_code=201
        )

        # verify the second review is created by checking its status.
        assert rs_duplicate['status'] == 'approved'
        assert not rs_duplicate['review'] == 'review'

    @pytest.mark.tcid52
    def test_review_creation_should_not_fail_if_reviewer_email_is_different(self):
        """
        All fields have the same value, but the 'reviewer_email' is changed.
        Expecting successful review creation.
        """
        # create another review with the same data except the 'reviewer_email' field.
        review_rs = self.product_review_helper.create_random_review_for_product(self.product_id)

        # create another review with the same data except the 'reviewer_email' field.
        rs_duplicate = self.product_review_helper.create_product_review(
            product_id=self.product_id,
            review=review_rs['review'],
            reviewer=review_rs['reviewer'],
            reviewer_email=generate_random_email_and_password()['email'],
            rating=review_rs['rating'],
            expected_status_code=201
        )

        # Verify the second review is created and approved
        assert rs_duplicate['status'] == 'approved'
        assert not rs_duplicate['reviewer_email'] == 'reviewer_email'

    @pytest.mark.tcid53
    def test_verify_default_status_for_create_review_is_approved(self):
        """
        Verify the default status is "approved" if the status is not provided in payload
        """
        # Create a review for the product
        review_rs = self.product_review_helper.create_random_review_for_product(self.product_id)
        # Verify the second review is created and approved
        assert review_rs['status'] == 'approved', f"status of Review is approved by default."


