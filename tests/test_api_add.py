import allure
from utils.attach import demowebshop_api_log
from allure_commons._allure import step
from selene import browser
from selene.support.conditions import have


def test_post_add_to_cart_in_details(api_url, setup_browser):
    url = f'{api_url}/addproducttocart/details/18/1'
    data_product = {"addtocart_18.EnteredQuantity": 7,
                    "addtocart_19.EnteredQuantity": 7}

    with step("Browser open"):
        browser.open('/')

    with allure.step('Make a request'):
        result = demowebshop_api_log(f'{url}', data=data_product)
        cookie = result.cookies.get("Nop.customer")

    with step("Set cookie from API"):
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    with step("Open cart"):
        browser.open('/cart')

    with step("Check one item presents"):
        browser.all('.cart-item-row').should(have.size(1))
        (browser.all('.cart-item-row').element_by(have.text('Digital SLR Camera - Black'))
         .element('[name^="itemquantity"]').should(have.value("7")))


def test_post_add_to_cart_in_catalog(api_url, setup_browser):
    url = f'{api_url}/addproducttocart/catalog/51/1/1'
    url2 = f'{api_url}/addproducttocart/catalog/52/1/1'
    url3 = f'{api_url}/addproducttocart/catalog/53/1/1'

    with step("Browser open"):
        browser.open('/')

    with allure.step('Make a request'):
        result = demowebshop_api_log(url)
        cookie = result.cookies.get("Nop.customer")
        result = demowebshop_api_log(url2, cookies={"Nop.customer": cookie})
        cookie = result.cookies.get("Nop.customer")
        demowebshop_api_log(url3, cookies={"Nop.customer": cookie})

    with step("Set cookie from API"):
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    with step("Open cart"):
        browser.open('/cart')

    with step("Check three item presents"):
        browser.all('.cart-item-row').should(have.size(3))
        (browser.all('.cart-item-row').element_by(have.text('3rd Album')))
        (browser.all('.cart-item-row').element_by(have.text('Music 2')))
        (browser.all('tr:nth-child(3)>td.product').element_by(have.text('Music 2')))

    with step("Check total"):
        browser.element('.order-total').should(have.exact_text("14.00"))
