from pricing.catalog import Catalog
from pricing.models import Product, UnknownCurrency, UnknownProduct


def make_catalog():
    return Catalog(
        [
            Product("MUG-01", "Mug", {"USD": 1200, "EUR": 1100}),
            Product("TEE-02", "T-shirt", {"USD": 2500, "EUR": 2300}),
            Product("CAP-03", "Cap", {"USD": 1999, "EUR": 1850}),
        ]
    )


def test_usd_price():
    catalog = make_catalog()
    assert catalog.get_price("MUG-01", "USD") == 1200


def test_eur_price():
    catalog = make_catalog()
    assert catalog.get_price("TEE-02", "EUR") == 2300


def test_usd_after_eur_lookup():
    catalog = make_catalog()
    catalog.get_price("MUG-01", "EUR")
    assert catalog.get_price("MUG-01", "USD") == 1200, "USD price must not be the EUR one"


def test_eur_after_usd_lookup():
    catalog = make_catalog()
    catalog.get_price("CAP-03", "USD")
    assert catalog.get_price("CAP-03", "EUR") == 1850


def test_repeat_lookup_is_cached():
    catalog = make_catalog()
    for _ in range(3):
        catalog.get_price("mug-01", "usd")
    assert catalog.misses == 1


def test_unknown_sku_and_currency():
    catalog = make_catalog()
    try:
        catalog.get_price("NOPE", "USD")
        assert False, "expected UnknownProduct"
    except UnknownProduct:
        pass
    try:
        catalog.get_price("MUG-01", "JPY")
        assert False, "expected UnknownCurrency"
    except UnknownCurrency:
        pass
