
from ecom_test.src.utilities.wooAPIUtility import WooAPIUtility
import logging as logger


class CouponsAPIHelper:
    def __init__(self):
        """
        class has an '__init__' method that initializes
        an instance of the WooAPIUtility class.
        """
        self.woo_api_utility = WooAPIUtility()

    def call_create_coupon(self, payload):
        """
        Method makes a POST request to create a 'new_coupon'
        by calling the post-method of the woo_api_utility instance.
        """
        logger.debug("Calling 'Create Coupon'.")
        return self.woo_api_utility.post('coupons', params=payload, expected_status_code=201)

    def call_retrieve_coupon(self, coupon_id):
        """
        Calling 'retrieve_coupon'the get method of
        the woo_api_utility instance with the coupon ID as a parameter.
        """
        logger.debug(f"Calling retrieve a coupon. coupon id: {coupon_id}")
        return self.woo_api_utility.get(f'coupons/{coupon_id}')

    def call_list_all_coupons(self, payload=None):
        """
        Calling 'list all coupons'.
        The get method of the woo_api_utility instance.
        """
        logger.debug("Calling list all coupons.")
        return self.woo_api_utility.get('coupons', params=payload)

    def call_delete_coupon(self, coupon_id, force=True):
        """
        This method makes a 'DELETE' request to delete a coupon.
        """
        logger.debug(f"Calling list all coupons.")
        return self.woo_api_utility.delete(f'coupons/{coupon_id}', params={"force": force})
