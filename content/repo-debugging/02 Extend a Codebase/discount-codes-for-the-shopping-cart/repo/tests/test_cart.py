from cart.models import Product
from cart.service import CartService


def make_service():
    return CartService([
        Product("MUG", "Mug", 1200, "standard"),
        Product("TEA", "Tea", 450, "food"),
    ])


def test_add_merges_quantities():
    svc = make_service()
    cid = svc.create_cart()
    svc.add_item(cid, "MUG", 1)
    svc.add_item(cid, "MUG", 2)
    assert svc.quote(cid).subtotal_cents == 3600


def test_remove_unknown_sku_raises():
    svc = make_service()
    cid = svc.create_cart()
    try:
        svc.remove_item(cid, "TEA")
    except KeyError:
        return
    assert False, "expected KeyError"
