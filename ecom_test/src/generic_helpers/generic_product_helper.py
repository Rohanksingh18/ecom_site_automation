
import logging as logger
import random

from ecom_test.src.api_helpers.ProductsAPIHelpers import ProductsAPIHelper
from ecom_test.src.utilities.generic_utilities import generate_random_string


class GenericProductHelper:
    """
    Helper class for working with products in an e-commerce system.
    """

    def __init__(self):
        # Initialize the ProductsAPIHelper
        self.products_api_helper = ProductsAPIHelper()

    def get_random_products(self, qty=1, **kwargs):
        """
         Gets random products using the 'products' API.
        It calls the products API with the given parameters in **kwargs, randomly selects the given number of products
        from the response and returns them.
        List of available properties: https://woocommerce.github.io/woocommerce-rest-api-docs/#product-properties
        Example function calls:
            get_random_products(qty=1, status=private, type=variable)
            get_random_products(qty=1, downloadable=True)

        :param qty: Number of products to return.
        :param kwargs: Additional keyword arguments to filter the products.
        :return: List of randomly selected products.
        """

        payload = {"per_page": 100}
        products = self.products_api_helper.call_list_products(payload=payload)

        return random.sample(products, int(qty))

    def get_product_detail_via_api(self, product_id):
        """
         Retrieves the details of a specific product using the product ID.

        :param product_id: ID of the product.
        :return: Product details.
        """
        return self.products_api_helper.call_get_product_by_id(product_id)

    def create_a_product(self, product_type="simple", **kwargs):
        """
         Creates a new product.

        :param product_type: Type of the product (default is "simple").
        :param kwargs: Additional keyword arguments to specify product properties.
        :return: Created product details.
        """

        # Generate some data for the new product
        payload = dict()
        payload['type'] = product_type

        # Set the 'name' property if not provided
        if 'name' not in kwargs.keys():
            payload['name'] = generate_random_string(20)
        # Set the 'regular_price' property if not provided
        if 'regular_price' not in kwargs.keys():
            payload['regular_price'] = str(round(random.uniform(10, 100), 2))

        payload.update(kwargs)

        # Make the API call to create the product
        product_rs = ProductsAPIHelper().call_create_product(payload)

        logger.info(f"Created product. product_id - {product_rs['id']}")

        return product_rs

    def delete_a_product(self, product_id, force=True):
        """
         Deletes a product with the given product ID.

        :param product_id: ID of the product to delete.
        :param force: Boolean flag to force deletion (default is True).
        :return: deletion result.
        """
        return ProductsAPIHelper().call_delete_product(product_id, force=force)
