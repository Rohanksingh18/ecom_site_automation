
import pytest
from ecom_test.src.api_helpers.ProductsAPIHelpers import ProductsAPIHelper
from ecom_test.src.dao.products_dao import ProductsDAO
from datetime import datetime, timedelta


@pytest.mark.regression
class TestListProductsWithFilter(object):

    # create a method to get the list of products with filter for a specific period of time from now
    @pytest.mark.tcid35
    def test_list_products_with_filter_after(self):
        # Create a payload data request to be sent
        x_days_from_now = 60  # variable for requesting data for last 60 days form now
        after_created_date = datetime.now().replace(microsecond=0) - timedelta(days=x_days_from_now)
        after_date = after_created_date.isoformat()  # ISO8601 date format
        pyload = dict()  # data will be in dictionary format (Jason format)
        pyload['after'] = after_date
        pyload['per_page'] = 100  # showing 100 products per page.

        # make an API call
        rs_api = ProductsAPIHelper().call_list_products(pyload)
        assert rs_api, f" Empty response for 'list products with filter'"

        # get the data from database
        db_products = ProductsDAO().get_products_created_after_given_date(after_date)

        # verify the responses to match DB
        assert len(rs_api) == len(db_products), f"products with filter 'after' returned unexpected number of products,"\
                                                f"Expected: {len(db_products)}, Actual: {len(rs_api)}"

        ids_in_api = [i['id'] for i in rs_api]  # product api id
        ids_in_db = [i['ID'] for i in db_products]  # product db id
        ids_diff = list(set(ids_in_api) - set(ids_in_db))  # difference between both ids as a list
        assert not ids_diff, f" List products with filter, product ids is mismatching in db"
