from cart.discounts import BuyOneGetOne, DiscountError, FixedOff, PercentOff
from cart.models import Product
from cart.service import CartService


def make_service():
    products = [
        Product("MUG", "Mug", 1200, "standard"),
        Product("TEA", "Tea", 450, "food"),
        Product("BOOK", "Notebook", 2000, "book"),
    ]
    codes = [
        PercentOff("SAVE10", 10),
        PercentOff("HALF", 50),
        FixedOff("TEN", 1000),
        BuyOneGetOne("BOGO-TEA", "TEA"),
    ]
    return CartService(products, discounts=codes)


def basket(svc):
    cid = svc.create_cart()
    svc.add_item(cid, "MUG", 2)
    svc.add_item(cid, "TEA", 3)
    return cid


def test_percent_off():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "SAVE10")
    q = svc.quote(cid)
    assert q.discount_cents == 375
    assert q.tax_cents == 410 + 85
    assert q.total_cents == 3870


def test_fixed_off_spread_over_lines():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "TEN")
    q = svc.quote(cid)
    assert [line.discount_cents for line in q.lines] == [640, 360]
    assert q.tax_cents == 334 + 69
    assert q.total_cents == 3153


def test_fixed_off_capped_at_amount_due():
    svc = make_service()
    cid = svc.create_cart()
    svc.add_item(cid, "TEA", 1)
    svc.apply_code(cid, "TEN")
    q = svc.quote(cid)
    assert q.discount_cents == 450
    assert q.total_cents == 0


def test_buy_one_get_one():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "BOGO-TEA")
    q = svc.quote(cid)
    assert q.discount_cents == 450
    assert q.total_cents == 3750 - 450 + 456 + 63


def test_bogo_stacks_with_percent_in_either_order():
    for order in (["BOGO-TEA", "SAVE10"], ["SAVE10", "BOGO-TEA"]):
        svc = make_service()
        cid = basket(svc)
        for code in order:
            svc.apply_code(cid, code)
        q = svc.quote(cid)
        assert q.discount_cents == 780, order
        assert q.tax_cents == 410 + 57, order
        assert q.total_cents == 3437, order


def test_percent_and_fixed_do_not_stack():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "SAVE10")
    for code in ("TEN", "HALF"):
        try:
            svc.apply_code(cid, code)
        except DiscountError:
            pass
        else:
            assert False, f"{code} should have been rejected"
    assert svc.quote(cid).discount_cents == 375


def test_unknown_and_duplicate_codes_rejected():
    svc = make_service()
    cid = basket(svc)
    try:
        svc.apply_code(cid, "NOPE")
        assert False, "unknown code accepted"
    except DiscountError:
        pass
    svc.apply_code(cid, "BOGO-TEA")
    try:
        svc.apply_code(cid, "BOGO-TEA")
        assert False, "duplicate code accepted"
    except DiscountError:
        pass
