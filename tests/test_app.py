import pytest
import base64
from .tool.assertions import assert_valid_schema

valid_credentials = base64.b64encode(b'Ivan:xxx').decode('utf-8')
headers = {'Authorization': 'Basic ' + valid_credentials}


@pytest.mark.home
class TestClass:
    def test_home_page(self, client):
        rv = client.get('/')
        assert rv.status_code == 401

    def test_auth_home_page(slef, client):
        rv = client.get('/', headers=headers)
        assert rv.status_code == 200
        assert rv.data == b"Hello! Do not try to spy me!"


@pytest.mark.product
class TestProduct:

    def test_get_product(self, client):
        rv = client.get('/api/v1/products/0', headers=headers)
        assert rv.status_code == 200
        assert_valid_schema(rv, 'product.json')

    def test_get_products(self, client):
        rv = client.get('/api/v1/products', headers=headers)
        assert rv.status_code == 200
        assert_valid_schema(rv, 'products.json')


@pytest.mark.basket
class TestCart:
    def test_add_empty_to_cart(self, client):
        rv = client.post('/api/v1/basket', headers=headers)
        assert rv.status_code == 200
        assert_valid_schema(rv, "message.json")

    def test_add_cart_server_error(self, client):
        rv = client.post('/api/v1/basket', headers=headers, data={"goodId": 0})
        assert rv.status_code == 500

    def test_add_product_to_cart(self, client, item):
        rv = client.post('/api/v1/basket', headers=headers, json=item.product)
        assert rv.status_code == 200
        assert_valid_schema(rv, "add_cart.json")
        item.access_token["access_token"] = rv.get_json()["access_token"]

    def test_get_shopping_cart(self, client, item):
        rv = client.get('/api/v1/basket', query_string=item.access_token, headers=headers)
        assert rv.status_code == 200
        assert_valid_schema(rv, "basket_query.json")

    def test_delete_product_from_cart(self, client, item):
        rv = client.delete('/api/v1/basket/1', query_string=item.access_token, headers=headers,
                           json=item.product)
        assert rv.status_code == 200
        assert_valid_schema(rv, "message.json")


@pytest.mark.checkout
class TestCheckout:
    def test_checkout(self, client):
        rv = client.get('/api/v1/checkout', headers=headers)
        assert rv.status_code == 405

    def test_checkout_success(self, client, item):
        rv = client.post(f'/api/v1/checkout', query_string=item.access_token, headers=headers,
                         json=item.checkout_list)
        assert rv.status_code == 200
        assert_valid_schema(rv, "checkout.json")
        item.orderId["orderId"] = rv.get_json()["orderId"]


@pytest.mark.complete
class TestComplete:
    def test_complete(self, client, item):
        data = {**item.access_token, **item.orderId}
        rv = client.get('/api/v1/complete', query_string=data, headers=headers)
        assert rv.status_code == 200
        assert_valid_schema(rv, "complete.json")
