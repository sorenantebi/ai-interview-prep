from datetime import date

from pricing.catalog import Catalog
from pricing.discounts import CouponBook, SaleSchedule, apply_discounts
from pricing.models import (
    Coupon,
    Product,
    Sale,
    UnknownCurrency,
)
from pricing.service import PricingService
from pricing.utils import format_money, percent_off

APRIL = date(2026, 4, 10)
MARCH = date(2026, 3, 10)


def make_catalog():
    return Catalog(
        [
            Product("MUG-01", "Mug", {"USD": 1200, "EUR": 1100}),
            Product("TEE-02", "T-shirt", {"USD": 2500, "EUR": 2300}),
            Product("CAP-03", "Cap", {"USD": 1999, "EUR": 1850}),
        ]
    )


def spring_sale():
    return Sale(
        name="Spring",
        percent=20,
        skus=frozenset({"MUG-01", "TEE-02"}),
        start=date(2026, 3, 1),
        end=date(2026, 3, 31),
    )


def make_service(extra_sales=(), extra_coupons=()):
    sales = SaleSchedule([spring_sale(), *extra_sales])
    coupons = CouponBook([Coupon("WELCOME10", 10), Coupon("VIP25", 25), *extra_coupons])
    return PricingService(make_catalog(), sales, coupons)


def test_apply_discounts_both():
    sale = spring_sale()
    assert apply_discounts(1000, sale=sale, coupon=Coupon("X", 10)) == 720


def test_apply_discounts_single_and_none():
    assert apply_discounts(1000) == 1000
    assert apply_discounts(1000, sale=spring_sale()) == 800
    assert apply_discounts(1000, coupon=Coupon("X", 25)) == 750


def test_percent_off_rounding():
    assert percent_off(999, 15) == 849
    assert percent_off(5, 50) == 2
    assert percent_off(0, 30) == 0
    try:
        percent_off(100, 101)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_format_money():
    assert format_money(1999, "USD") == "$19.99"
    assert format_money(5, "EUR") == "EUR 0.05"


def test_usd_after_eur_for_every_sku():
    catalog = make_catalog()
    for sku, usd, eur in [("MUG-01", 1200, 1100), ("TEE-02", 2500, 2300), ("CAP-03", 1999, 1850)]:
        assert catalog.get_price(sku, "EUR") == eur
        assert catalog.get_price(sku, "USD") == usd


def test_cache_misses_per_currency():
    catalog = make_catalog()
    for currency in ["USD", "EUR", "USD", "EUR", "USD"]:
        catalog.get_price("MUG-01", currency)
    assert catalog.misses == 2


def test_currency_case_shares_cache_entry():
    catalog = make_catalog()
    assert catalog.get_price("MUG-01", "eur") == 1100
    assert catalog.get_price("MUG-01", " EUR ") == 1100
    assert catalog.misses == 1


def test_failed_lookup_is_not_cached():
    catalog = make_catalog()
    for _ in range(2):
        try:
            catalog.get_price("MUG-01", "JPY")
            assert False, "expected UnknownCurrency"
        except UnknownCurrency:
            pass
    assert catalog.get_price("MUG-01", "USD") == 1200


def test_clear_cache_forces_new_lookup():
    catalog = make_catalog()
    catalog.get_price("CAP-03", "EUR")
    catalog.clear_cache()
    catalog.get_price("CAP-03", "EUR")
    assert catalog.misses == 2


def test_catalogs_do_not_share_cache():
    first, second = make_catalog(), make_catalog()
    first.get_price("MUG-01", "USD")
    second.get_price("MUG-01", "EUR")
    assert first.get_price("MUG-01", "USD") == 1200
    assert second.get_price("MUG-01", "EUR") == 1100


def test_quote_fields_with_sale_and_coupon():
    quote = make_service().quote("MUG-01", 1, "USD", "WELCOME10", on=MARCH)
    assert quote.list_unit_price == 1200
    assert quote.sale_unit_price == 960
    assert quote.total == 864
    assert quote.sale_name == "Spring"
    assert quote.coupon_code == "WELCOME10"


def test_sale_only_quote_has_no_coupon():
    quote = make_service().quote("TEE-02", 1, "USD", on=MARCH)
    assert quote.coupon_code is None
    assert quote.total == 2000


def test_lowercase_sku_and_coupon_with_sale():
    quote = make_service().quote("mug-01", 1, "usd", "welcome10", on=MARCH)
    assert quote.total == 864
    assert quote.currency == "USD"


def test_eur_sale_and_coupon():
    quote = make_service().quote("MUG-01", 1, "EUR", "WELCOME10", on=MARCH)
    assert quote.total == 792


def test_overlapping_sales_best_wins_then_coupon():
    flash = Sale("Flash", 30, frozenset({"MUG-01"}), date(2026, 3, 10), date(2026, 3, 12))
    service = make_service(extra_sales=[flash])
    assert service.quote("MUG-01", 1, "USD", on=date(2026, 3, 11)).total == 840
    assert service.quote("MUG-01", 1, "USD", "WELCOME10", on=date(2026, 3, 11)).total == 756
    assert service.quote("MUG-01", 1, "USD", on=date(2026, 3, 13)).total == 960


def test_full_discount_coupon():
    service = make_service(extra_coupons=[Coupon("FREE", 100)])
    assert service.quote("MUG-01", 2, "USD", "FREE", on=MARCH).total == 0


def test_cart_total_with_sale_and_coupon_in_eur():
    service = make_service()
    items = [("MUG-01", 1), ("TEE-02", 1), ("CAP-03", 1)]
    assert service.cart_total(items, "EUR", "WELCOME10", on=MARCH) == 4113


def test_cart_totals_in_two_currencies_on_one_service():
    service = make_service()
    items = [("MUG-01", 1), ("TEE-02", 1)]
    assert service.cart_total(items, "USD", on=APRIL) == 3700
    assert service.cart_total(items, "EUR", on=APRIL) == 3400
    assert service.cart_total(items, "USD", on=APRIL) == 3700


def test_invalid_quantity():
    try:
        make_service().quote("MUG-01", 0, "USD", on=APRIL)
        assert False, "expected ValueError"
    except ValueError:
        pass
