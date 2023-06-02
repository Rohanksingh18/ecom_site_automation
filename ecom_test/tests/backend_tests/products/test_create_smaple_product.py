
import pytest
from Ecom_test.src.utilities.generic_utilities import generate_random_string
from Ecom_test.src.api_helpers.ProductsAPIHelpers import ProductsAPIHelper
from Ecom_test.src.dao.products_dao import ProductsDAO

pytestmark = [pytest.mark.products, pytest.mark.smoke, pytest.mark.BE]

@pytest.mark.tcid34

# create a subclass to create a sample product
def test_create_a_sample_product():

    #create payload with some data for prduct discription
    payload = dict() # data will be in dictionary format (Jason format)
    payload['name'] = generate_random_string(10) #will generate random name for the product
    payload['type'] = "sample" #will define the type of product
    payload['price'] = "18.99" #price of the sample product

    # make an API call to create a sample product
    product_sample = ProductsAPIHelper().call_create_product(payload) # calling product helpers to create a product with data in the payload

    # verify that response is not empty
    assert product_sample, f"sample product create is empty.Payload: {payload}"
    assert product_sample['name']== payload['name'], f"sample product create api call response name is not matching \." \
                                                     f" Expected name: {payload['name']}, Actual name: {product_sample['name']}"

    # verify the database that product is exists by checking product id
    product_sample_id = product_sample['id']
    db_sample_product = ProductsDAO().get_product_by_id(product_sample_id)
    assert payload['name'] == db_sample_product[0]['post_title'], f"sample product create, title in db does not match " \
                                                                  f"title in api. DB: {db_sample_product['post_title']}, API: {payload['name']}"

