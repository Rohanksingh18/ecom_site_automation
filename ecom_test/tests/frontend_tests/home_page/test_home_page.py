import pytest
from ecom_test.src.pages.HomePage import HomePage
from ecom_test.src.pages.Header import Header

# These markers can be used to selectively run or exclude tests based on their assigned markers.
pytestmark = [pytest.mark.fe, pytest.mark.regression, pytest.mark.smoke, pytest.mark.home_page]


@pytest.mark.usefixtures('init_driver')
class TestHomePageSmoke:

    @pytest.fixture(scope='class')  # to perform any home_page related tests, it needed to be on home_page.
    def setup(self, request):  # request argument to access the fixture objects.
        request.cls.homepage = HomePage(self.driver)
        request.cls.header = Header(self.driver)
        self.homepage.go_to_the_home_page()

        yield

    # Verify home page displays 12 products (Total no of products page=12), tcid4.
    @pytest.mark.tcid4
    def test_verify_no_of_products_displayed(self, setup):
        expected_no_of_products = 12  # from home_page display.
        all_product_elements = self.homepage.get_all_product_elements()

        # verify by comparing
        assert len(all_product_elements) == expected_no_of_products,\
            f" Number of products displayed on the home_page is unexpected"\
            f" Expected: {expected_no_of_products}, Actual: {len(all_product_elements)}"

    # Verify heading (Header= Shop) on the home_page is displayed, tcid5.
    @pytest.mark.tcid5
    def test_heading_is_displayed(self,setup):
        expected_header = 'Shop'  # from ecom-site.
        displayed_header = self.homepage.get_displayed_heading()

        # verifying by comparing.
        assert displayed_header == expected_header, f"Wrong heading displayed"\
                                                    f"Expected: {expected_header}, Actual: {displayed_header}"

    # Verify the header menu is displayed, tcid6.
    @pytest.mark.tcid6
    def test_header_menu_is_displayed(self, setup):
        self.header.assert_all_menu_items_displayed()