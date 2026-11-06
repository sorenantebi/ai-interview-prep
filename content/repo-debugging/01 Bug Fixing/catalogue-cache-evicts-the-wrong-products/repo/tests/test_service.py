from catalog.cache import LRUCache
from catalog.models import Product
from catalog.service import CatalogService, ProductNotFound


def make_service(cache=None):
    products = [
        Product(1, "Atlas", "books", 1999),
        Product(2, "Bible of Bash", "books", 2450),
        Product(3, "Kettle", "kitchen", 3500),
        Product(4, "Toaster", "kitchen", 2900),
    ]
    return CatalogService(products, cache)


def test_get_product_is_cached():
    service = make_service()
    service.get_product(1)
    service.get_product(1)
    assert service.loads == 1


def test_unknown_product_raises():
    service = make_service()
    try:
        service.get_product(99)
    except ProductNotFound:
        return
    assert False, "expected ProductNotFound"


def test_list_category_sorted_by_name():
    service = make_service()
    names = [p.name for p in service.list_category("books")]
    assert names == ["Atlas", "Bible of Bash"]


def test_update_price_only_invalidates_own_category():
    service = make_service()
    service.get_product(1)
    service.get_product(3)
    service.update_price(1, 2100)
    loads_before = service.loads
    service.get_product(3)
    assert service.loads == loads_before, "kitchen product should still be cached"
    service.get_product(1)
    assert service.loads == loads_before + 1


def test_describe_uses_current_price():
    service = make_service()
    assert service.describe(1) == "Atlas: 19.99 EUR"
    service.update_price(1, 2100)
    assert service.describe(1) == "Atlas: 21.00 EUR"


def test_busy_product_stays_cached_in_small_cache():
    service = make_service(LRUCache(2))
    service.get_product(1)
    service.get_product(2)
    service.get_product(1)
    service.get_product(3)
    loads_before = service.loads
    service.get_product(1)
    assert service.loads == loads_before, "product 1 was just used and should be cached"
