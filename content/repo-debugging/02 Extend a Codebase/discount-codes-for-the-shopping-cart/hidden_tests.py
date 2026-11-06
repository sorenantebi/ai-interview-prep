from cart.discounts import BuyOneGetOne, DiscountError, FixedOff, PercentOff
from cart.models import Product
from cart.service import CartService


def make_service():
    products = [
        Product("MUG", "Mug", 1200, "standard"),
        Product("TEA", "Tea", 450, "food"),
        Product("BOOK", "Notebook", 2000, "book"),
        Product("PEN", "Pen", 199, "standard"),
        Product("A", "A", 100, "standard"),
        Product("B", "B", 100, "standard"),
        Product("C", "C", 100, "standard"),
    ]
    codes = [
        PercentOff("SAVE10", 10),
        PercentOff("HALF", 50),
        PercentOff("FREE", 100),
        FixedOff("TEN", 1000),
        FixedOff("OFF100", 100),
        BuyOneGetOne("BOGO-TEA", "TEA"),
        BuyOneGetOne("BOGO-TEA-2", "TEA"),
        BuyOneGetOne("BOGO-MUG", "MUG"),
    ]
    return CartService(products, discounts=codes)


def basket(svc):
    cid = svc.create_cart()
    svc.add_item(cid, "MUG", 2)
    svc.add_item(cid, "TEA", 3)
    return cid


def rejected(fn, *args):
    try:
        fn(*args)
    except DiscountError:
        return True
    return False


def test_codes_are_case_insensitive_and_trimmed():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "  save10 ")
    assert svc.quote(cid).discount_cents == 375
    assert rejected(svc.apply_code, cid, "SAVE10")


def test_bogo_on_different_skus_stack():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "BOGO-MUG")
    svc.apply_code(cid, "BOGO-TEA")
    q = svc.quote(cid)
    assert q.discount_cents == 1650
    assert q.tax_cents == 228 + 63
    assert q.total_cents == 2391


def test_two_bogo_on_same_sku_rejected():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "BOGO-TEA")
    assert rejected(svc.apply_code, cid, "BOGO-TEA-2")
    assert svc.quote(cid).discount_cents == 450


def test_bogo_odd_quantities():
    for qty, expected in ((1, 0), (2, 450), (3, 450), (5, 900)):
        svc = make_service()
        cid = svc.create_cart()
        svc.add_item(cid, "TEA", qty)
        svc.apply_code(cid, "BOGO-TEA")
        assert svc.quote(cid).discount_cents == expected, qty


def test_bogo_for_sku_not_in_cart_has_no_effect_until_added():
    svc = make_service()
    cid = svc.create_cart()
    svc.add_item(cid, "MUG", 1)
    svc.apply_code(cid, "BOGO-TEA")
    assert svc.quote(cid).discount_cents == 0
    svc.add_item(cid, "TEA", 2)
    assert svc.quote(cid).discount_cents == 450


def test_percent_rounds_half_up_per_line():
    svc = make_service()
    cid = svc.create_cart()
    svc.add_item(cid, "PEN", 1)
    svc.apply_code(cid, "HALF")
    q = svc.quote(cid)
    assert q.discount_cents == 100
    assert q.tax_cents == 19
    assert q.total_cents == 118


def test_fixed_remainder_goes_to_earlier_lines():
    svc = make_service()
    cid = svc.create_cart()
    for sku in ("C", "A", "B"):
        svc.add_item(cid, sku, 1)
    svc.apply_code(cid, "OFF100")
    q = svc.quote(cid)
    assert [line.sku for line in q.lines] == ["A", "B", "C"]
    assert [line.discount_cents for line in q.lines] == [34, 33, 33]
    assert q.discount_cents == 100
    assert q.total_cents == 239


def test_fixed_is_capped_after_bogo():
    svc = make_service()
    cid = svc.create_cart()
    svc.add_item(cid, "TEA", 2)
    svc.apply_code(cid, "TEN")
    svc.apply_code(cid, "BOGO-TEA")
    q = svc.quote(cid)
    assert q.discount_cents == 900
    assert q.tax_cents == 0
    assert q.total_cents == 0


def test_percent_applies_to_amount_after_bogo():
    svc = make_service()
    cid = svc.create_cart()
    svc.add_item(cid, "TEA", 2)
    svc.apply_code(cid, "HALF")
    svc.apply_code(cid, "BOGO-TEA")
    q = svc.quote(cid)
    assert q.discount_cents == 675
    assert q.tax_cents == 16
    assert q.total_cents == 241


def test_remove_code_frees_the_cart_wide_slot():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "SAVE10")
    svc.remove_code(cid, " save10")
    assert svc.quote(cid).discount_cents == 0
    svc.apply_code(cid, "TEN")
    assert svc.quote(cid).discount_cents == 1000
    assert rejected(svc.remove_code, cid, "SAVE10")


def test_carts_are_independent_and_quotes_repeatable():
    svc = make_service()
    first = basket(svc)
    second = basket(svc)
    svc.apply_code(first, "SAVE10")
    assert svc.quote(second).discount_cents == 0
    assert svc.quote(first) == svc.quote(first)
    assert svc.quote(first).subtotal_cents == 3750


def test_hundred_percent_off_is_free():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "FREE")
    q = svc.quote(cid)
    assert q.discount_cents == 3750
    assert q.tax_cents == 0
    assert q.total_cents == 0


def test_line_figures_add_up_to_quote():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "BOGO-TEA")
    svc.apply_code(cid, "SAVE10")
    q = svc.quote(cid)
    assert sum(l.discount_cents for l in q.lines) == q.discount_cents
    for line in q.lines:
        assert line.net_cents == line.gross_cents - line.discount_cents
    assert sum(l.net_cents + l.tax_cents for l in q.lines) == q.total_cents


def test_fixed_off_on_empty_cart():
    svc = make_service()
    cid = svc.create_cart()
    svc.apply_code(cid, "TEN")
    q = svc.quote(cid)
    assert q.lines == []
    assert q.discount_cents == 0
    assert q.total_cents == 0


def test_fixed_then_percent_rejected_and_unknown_cart():
    svc = make_service()
    cid = basket(svc)
    svc.apply_code(cid, "TEN")
    assert rejected(svc.apply_code, cid, "SAVE10")
    assert svc.quote(cid).discount_cents == 1000
    try:
        svc.apply_code(999, "TEN")
    except KeyError:
        return
    assert False, "expected KeyError for unknown cart"
