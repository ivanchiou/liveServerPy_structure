import pytest
import json
import base64

valid_credentials = base64.b64encode(b'Ivan:xxx').decode('utf-8')
headers = {'Authorization': 'Basic ' + valid_credentials}


def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 401


def test_auth_home_page(client):
    rv = client.get('/', headers=headers)
    assert rv.status_code == 200
    assert rv.data == b"Hello! Do not try to spy me!"


def test_get_products(client):
    rv = client.get('/api/v1/products', headers=headers)
    assert rv.status_code == 200
    data = json.loads(rv.data.decode())[0]
    assert data['category'] == '時尚'
    assert data['cateId'] == 11
    assert data['data'][0]['goodId'] == 0
    assert data['data'][0]['name'] == 'Samsung Galaxy S10+ 6.4吋智慧型手機 8G/128G'
    assert data['data'][0]['price'] == 0
    assert data['data'][0]['image'] == 'https://ehs-shop.tyson711.now.sh/static/images/470x600-01.jpg'
    assert data['data'][0]['description'] == 'This is description'
    assert data['data'][0]['stylesId'] == 'a0015,a0016'
    assert data['data'][0]['promoMsg'] == '30% OFF'


def test_get_shopping_cart(client):
    rv = client.get('/api/v1/basket', headers=headers)
    assert rv.status_code == 200


def test_checkout(client):
    rv = client.get('/api/v1/checkout', headers=headers)
    assert rv.status_code == 405


def test_complete(client):
    rv = client.get('/api/v1/complete', headers=headers)
    assert rv.status_code == 200
