
from ecom_test.src.utilities.wooAPIUtility import WooAPIUtility
import logging as logger


class CouponsAPIHelper:
    # class has an __init__ method that initializes an instance of the WooAPIUtility class.
    def __init__(self):
        self.woo_api_utility = WooAPIUtility()

    # Method makes a POST request to create a new coupon by calling the post-method of the woo_api_utility instance.
    def call_create_coupon(self, payload):
        logger.debug("Calling 'Create Coupon'.")
        return self.woo_api_utility.post('coupons', params=payload, expected_status_code=201)

    #  Calling the get method of the woo_api_utility instance with the coupon ID as a parameter.
    def call_retrieve_coupon(self, coupon_id):
        logger.debug(f"Calling retrieve a coupon. Coupon id: {coupon_id}")
        return self.woo_api_utility.get(f'coupons/{coupon_id}')

    # calling the get method of the woo_api_utility instance.
    def call_list_all_coupons(self, payload=None):
        logger.debug("Calling list all coupons.")
        return self.woo_api_utility.get('coupons', params=payload)

    # This method makes a DELETE request to delete a coupon.
    def call_delete_coupon(self, coupon_id, force=True):
        logger.debug(f"Calling list all coupons.")
        return self.woo_api_utility.delete(f'coupons/{coupon_id}', params={"force": force})
