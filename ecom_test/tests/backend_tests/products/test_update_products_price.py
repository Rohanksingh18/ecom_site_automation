import pytest
from ecom_test.src.api_helpers.ProductsAPIHelpers import ProductsAPIHelper
from ecom_test.src.utilities.generic_utilities import generate_random_string
import random

pytestmark = [pytest.mark.products, pytest.mark.regression]


@pytest.mark.tcid36
def test_update_regular_price_updates_price():
    # Retrieve a random product from the database that are not on_sale.
    product_helper = ProductsAPIHelper()
    filters = {'on_sale': False, 'per_page': 100}
    random_product = product_helper.call_list_products(filters)

    if random_product:
        selected_product = random.choice(random_product)
        product_id = selected_product['id']
    else:
        # if no product that on_sale=False, then take a random product and update the data.
        rand_products = product_helper.call_list_products()
        selected_product = random.choice(rand_products)
        product_id = selected_product['id']
        product_helper.call_update_product(product_id, {'sale_price': ''})

        # make the random update to the 'regular_price'
        new_price = str(random.randint(10, 100)) + '.' + str(random.randint(10, 99))
        payload = dict()
        payload['regular_price'] = new_price
        updated_rs = product_helper.call_update_product(product_id, payload=payload)

        # Verify the update of 'regular_price' field
        assert updated_rs['regular_price'] == new_price

        # Verify the update of 'price' field
        assert updated_rs['price'] == new_price

        # get the product after the update and verify response
        updated_rs = product_helper.call_retrieve_product(product_id)
        assert updated_rs['regular_price'] == new_price, f"Update product api call response. Updating the " \
                                                         f"'regular_price' did not " \
                                                         f"update. Actual 'regular_price'={updated_rs['price']}," \
                                                         f"but expected: {new_price}"
        assert updated_rs['price'] == new_price, f"Update product api call response. Updating the 'regular_price' did " \
                                                 f"not " \
                                                 f"update the 'price' field. price field actual value {updated_rs['price']}," \
                                                 f"but expected: {new_price}"


@pytest.mark.tcid37
@pytest.mark.tcid38
def test_update_sales_field_by_updating_sales_price():
    """
    "update the sale_price > 0, and verify that 'on_sale' is set to True"
    :return: on_sale= True
    """
    # create a random product with payloads for the test and verify the product has on_sale=False.
    product_helper = ProductsAPIHelper()
    regular_price = str(random.randint(10, 100)) + '.' + str(
        random.randint(10, 99))  # generating random price rate with defining limits.
    payload = dict()  # json format
    payload['name'] = generate_random_string(15)
    payload['type'] = "simple"
    payload['regular_price'] = regular_price
    product_info = product_helper.call_create_product(payload)
    product_id = product_info['id']
    assert not product_info['on_sale'], f" new product should not have 'on_sale=true'. Product id: {product_id}"
    assert not product_info['sale_price'], f" the new product should not have the value for 'sale_price'option"

    # tcid37- update the sale_price and verify that 'on_sale' is set to true.
    sale_price = float(regular_price) * 0.8  # Here updating the new sale_price by adding 20% discount on the product.
    product_helper.call_update_product(product_id, {'sale_price': str(sale_price)})  # updating the new sale_price.
    sale_price_after_update = product_helper.call_retrieve_product(product_id)  # getting updated new sale_price
    assert sale_price_after_update['on_sale'], f" sale_price after update, though the on_sale field is still false.\"" \
                                               f"product_id: {product_id}"  # verifying

    #  tcid38 update the sale_price to empty string and verify 'on_sale' field is set to false

    product_helper.call_update_product(product_id, {'sale_price': ''})
    sale_price_after_update = product_helper.call_retrieve_product(product_id)
    assert not sale_price_after_update['on_sale'], f"new 'sale_price=""' of product, but 'on_sale' is 'False'." \
                                                   f"Product id: {product_id}"


# verify that after updating sale_price, it updates the sale_price field or 'on_sale'=True
@pytest.mark.tcid39
def test_updated_sale_price_updates_on_sale_true():
    # getting a product from DB, which is not on_sale
    product_helper = ProductsAPIHelper()
    filters = {'on_sale': False, 'per_page': 100}
    random_product = product_helper.call_list_products(filters)
    selected_product = random.choice(random_product)
    product_id = selected_product['id']

    # check the status of on_sale is false
    info = product_helper.call_retrieve_product(product_id)  # retrieving the original information
    assert not info['on_sale'], f" test data with tag on_sale=False. though got True tag"

    # update the sale_price of the selected product
    sale_price = float(info['regular_price']) * 0.8  # Here updating the new sale_price by\
    # adding a 20 % discount on the selected product.
    pyload = dict()
    pyload['sale_price'] = str(sale_price)
    product_helper.call_update_product(product_id, payload=pyload)

    # verify the product sale_price is updated
    after_info = product_helper.call_retrieve_product(product_id)
    assert after_info['sale_price'] == str(sale_price), f"Updated product 'sale_price' however value did not matched." \
                                                        f"Product id: {product_id}, Expected sale price: {sale_price}," \
                                                        f"Actual sale price: {after_info['sale_price']}"

