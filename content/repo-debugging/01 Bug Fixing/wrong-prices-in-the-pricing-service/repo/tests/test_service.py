from datetime import date

from pricing.catalog import Catalog
from pricing.discounts import CouponBook, SaleSchedule
from pricing.models import Coupon, Product, Sale, UnknownCoupon
from pricing.service import PricingService

APRIL = date(2026, 4, 10)
MARCH = date(2026, 3, 10)


def make_service():
    catalog = Catalog(
        [
            Product("MUG-01", "Mug", {"USD": 1200, "EUR": 1100}),
            Product("TEE-02", "T-shirt", {"USD": 2500, "EUR": 2300}),
            Product("CAP-03", "Cap", {"USD": 1999, "EUR": 1850}),
        ]
    )
    spring = Sale(
        name="Spring",
        percent=20,
        skus=frozenset({"MUG-01", "TEE-02"}),
        start=date(2026, 3, 1),
        end=date(2026, 3, 31),
    )
    coupons = CouponBook([Coupon("WELCOME10", 10), Coupon("VIP25", 25)])
    return PricingService(catalog, SaleSchedule([spring]), coupons)


def test_no_discounts():
    quote = make_service().quote("MUG-01", 2, "USD", on=APRIL)
    assert quote.total == 2400


def test_sale_only():
    quote = make_service().quote("MUG-01", 3, "USD", on=MARCH)
    assert quote.sale_unit_price == 960
    assert quote.total == 2880
    assert quote.sale_name == "Spring"


def test_coupon_only():
    quote = make_service().quote("MUG-01", 1, "USD", "WELCOME10", on=APRIL)
    assert quote.total == 1080


def test_sale_and_coupon():
    quote = make_service().quote("MUG-01", 1, "USD", "WELCOME10", on=MARCH)
    assert quote.total == 864, "20% sale then 10% coupon on 1200"
    quote = make_service().quote("TEE-02", 2, "USD", "VIP25", on=MARCH)
    assert quote.total == 3000


def test_sale_window_is_inclusive():
    service = make_service()
    assert service.quote("MUG-01", 1, on=date(2026, 3, 1)).total == 960
    assert service.quote("MUG-01", 1, on=date(2026, 3, 31)).total == 960
    assert service.quote("MUG-01", 1, on=date(2026, 2, 28)).total == 1200
    assert service.quote("MUG-01", 1, on=date(2026, 4, 1)).total == 1200


def test_mixed_currencies_on_one_service():
    service = make_service()
    assert service.quote("MUG-01", 1, "USD", on=MARCH).total == 960
    eur = service.quote("MUG-01", 1, "EUR", on=MARCH)
    assert eur.list_unit_price == 1100
    assert eur.total == 880


def test_unknown_coupon_raises():
    try:
        make_service().quote("MUG-01", 1, "USD", "NOSUCH", on=APRIL)
        assert False, "expected UnknownCoupon"
    except UnknownCoupon:
        pass


def test_cart_total():
    service = make_service()
    assert service.cart_total([("MUG-01", 1), ("TEE-02", 2)], "USD", on=APRIL) == 6200
    assert service.cart_total([("CAP-03", 1)], "EUR", on=APRIL) == 1850
