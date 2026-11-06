from cart.models import Product
from cart.service import CartService
from cart.tax import TaxTable


def make_service():
    return CartService([
        Product("MUG", "Mug", 1200, "standard"),
        Product("TEA", "Tea", 450, "food"),
    ])


def test_quote_without_discounts():
    svc = make_service()
    cid = svc.create_cart()
    svc.add_item(cid, "MUG", 2)
    svc.add_item(cid, "TEA", 3)
    q = svc.quote(cid)
    assert q.subtotal_cents == 3750
    assert q.discount_cents == 0
    assert q.tax_cents == 456 + 95
    assert q.total_cents == 4301


def test_tax_rounds_half_up():
    assert TaxTable().tax_for("food", 50) == 4
