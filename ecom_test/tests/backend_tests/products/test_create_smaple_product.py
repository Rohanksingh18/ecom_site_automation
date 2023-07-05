import pytest
from ecom_test.src.utilities.generic_utilities import generate_random_string
from ecom_test.src.api_helpers.ProductsAPIHelpers import ProductsAPIHelper
from ecom_test.src.dao.products_dao import ProductsDAO

# These markers can be used to selectively run or exclude tests based on their assigned markers.
pytestmark = [pytest.mark.products, pytest.mark.smoke, pytest.mark.BE]


@pytest.mark.tcid34
def test_create_a_sample_product():
    """
    Test case: Verify 'POST /products' creates a sample product.
    Create a payload data requests to send for product description.
    Data will be in dictionary format (Json format).
    """
    payload = dict()
    payload['name'] = generate_random_string(10)  # will generate random name for the product
    payload['type'] = "simple"  # will define the type of product
    payload['price'] = "18.99"  # price of the sample product

    # make an API call to create a sample product
    product_sample = ProductsAPIHelper().call_create_product( payload)

    # verify that the response is not empty
    assert product_sample, f"sample product create is empty.Payload: {payload}"
    assert product_sample['name'] == payload['name'], f"sample product create api call response name is not matching."\
                                                      f" Expected name: {payload['name']},\
                                                      Actual name: {product_sample['name']}"

    # verify the database that product is existed by checking product id
    product_sample_id = product_sample['id']
    db_sample_product = ProductsDAO().get_product_by_id(product_sample_id)
    assert payload['name'] == db_sample_product[0]['post_title'], f"sample product create, title in db does not match "\
                                                                  f"title in api. DB: {db_sample_product['post_title']}\
                                                                  ,API: {payload['name']}"

