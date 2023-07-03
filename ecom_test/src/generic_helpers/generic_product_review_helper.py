
from ecom_test.src.utilities.generic_utilities import generate_random_string, generate_random_email_and_password
from ecom_test.src.utilities.wooAPIUtility import WooAPIUtility


class GenericProductReviewsHelper:
    """
    Helper class for managing product reviews in an e-commerce system.
    """

    def __init__(self):
        # Initialize the WooAPIUtility for making API calls
        self.woo_api_utility = WooAPIUtility()

    def create_product_review(self, product_id, review, reviewer, reviewer_email, rating, expected_status_code=201, **kwargs):
        """
         Create a product review (Payload) for a specific product.

        :param product_id: The ID of the product to review.
        :param review: The text content of the review.
        :param reviewer: The name of the reviewer.
        :param reviewer_email: The email address of the reviewer.
        :param rating: The rating given to the product (integer value).
        :param expected_status_code: The expected HTTP status code (default is 201).
        :param kwargs: Additional keyword arguments to include in the payload.
        :return: The response from the API call.
        """
        payload = {
            "product_id": product_id,
            "review": review,
            "reviewer": reviewer,
            "reviewer_email": reviewer_email,
            "rating": rating
        }

        payload.update(kwargs)

        return self.woo_api_utility.post('products/reviews', params=payload, expected_status_code=expected_status_code)

    def get_product_review(self, review_id, expected_status_code=200):
        """
         Get a specific product review by its ID.

        :param review_id: The ID of the review.
        :param expected_status_code: The expected HTTP status code (default is 200).
        :return: The response from the API call.
        """
        return self.woo_api_utility.get(f'products/reviews/{review_id}', expected_status_code=expected_status_code)

    def create_random_review_for_product(self, product_id):
        """
        Create a random review for a specific product.

        :param product_id: The ID of the product to review.
        :return: The response from the API call.
        """
        # Generate random reviewer name
        random_name = f"{generate_random_string(length=5)} {generate_random_string(length=6)}"
        # Generate random reviewer email
        random_email = generate_random_email_and_password()['email']
        # Generate random review content
        random_review = "Automation demo review: " + generate_random_string(length=25)

        return self.create_product_review(product_id, review=random_review, reviewer=random_name, reviewer_email=random_email, rating=5)
