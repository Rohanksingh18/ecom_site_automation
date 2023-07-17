

import random
from datetime import datetime
import string
from ecom_test.src.api_helpers.CouponsAPIHelper import CouponsAPIHelper


class GenericCouponHelper:

    def __init__(self):
        self.coupon_api_helper = CouponsAPIHelper()

    def create_coupon(self, coupon_code=None, length=4, expired=False, discount_type="percent", amount="100"):

        if expired:
            expiration_date = datetime.now().isoformat()
        else:
            expiration_date = None

        if not coupon_code:
            coupon_code = ''.join(random.choice(string.ascii_uppercase) for i in range(length))

        payload = {
            "code": coupon_code,
            "discount_type": discount_type,
            "amount": amount,
            "date_expires": expiration_date
        }

        rs_api = self.coupon_api_helper.call_create_coupon(payload=payload)
        coupon_code = rs_api["code"]

        return coupon_code

    def delete_coupon(self, coupon_code=None, coupon_id=None):

        if coupon_code and coupon_id:
            raise Exception(f"Must pass in 'coupon_code' or 'coupon_id' not both.")
        if not coupon_code and not coupon_id:
            raise Exception("Either coupon_code or coupon_id must be provided to delete a coupon.")

        if coupon_code:
            # since the coupon_code is given, get the coupon_id to use for deletion
            payload = {"code": coupon_code}
            rs_api = self.coupon_api_helper.call_list_all_coupons(payload=payload)
            coupon_id = rs_api[0]['id']

        # delete the coupon
        self.coupon_api_helper.call_delete_coupon(coupon_id=coupon_id)

    def get_coupon_info_by_coupon_code(self, coupon_code):

        rs_api = self.coupon_api_helper.call_retrieve_coupon(coupon_code)
        assert rs_api.status_code == 200, f"Failed getting coupon by coupon code: {coupon_code}"

        return rs_api.json()