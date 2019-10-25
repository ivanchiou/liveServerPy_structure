from run import create_app
import pytest


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def item():
    return Item()


class Item:
    access_token = {"access_token": None}
    orderId = {"orderId": None}
    product = {"goodId": "1",
               "styleId": "a0016",
               "quantity": "5"}
    checkout_list = {
        "products": [
            {
                "goodId": 3,
                "quantity": 2
            }
        ],
        "payment": 0,
        "invoice": 1,
        "receiver": {
            "name": "Ivan",
            "phone": "0900000000",
            "addr1": "新北市中和區",
            "addr2": "景平路258號"
        }
    }
