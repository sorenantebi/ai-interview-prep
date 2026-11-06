import random
import time
from collections import OrderedDict

from catalog.cache import LRUCache
from catalog.models import CacheEntry, Product
from catalog.service import CatalogService, ProductNotFound
from catalog.utils import format_price


def make_service(cache=None):
    products = [
        Product(1, "Atlas", "books", 1999),
        Product(2, "Bible of Bash", "books", 2450),
        Product(3, "Kettle", "kitchen", 3500),
        Product(4, "Toaster", "kitchen", 2900),
        Product(5, "Lamp", "home", 1500),
    ]
    return CatalogService(products, cache)


def test_capacity_validation():
    try:
        LRUCache(0)
    except ValueError:
        return
    assert False, "capacity 0 must be rejected"


def test_get_reorders_keys():
    cache = LRUCache(3)
    for k in "abc":
        cache.put(k, k)
    cache.get("a")
    assert cache.keys() == ["b", "c", "a"]


def test_miss_does_not_change_order():
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("zzz")
    assert cache.keys() == ["a", "b"]


def test_put_existing_replaces_and_refreshes():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    cache.put("c", 3)
    assert "b" not in cache
    assert cache.get("a") == 10


def test_len_does_not_refresh():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert len(cache) == 2
    cache.put("c", 3)
    assert cache.keys() == ["b", "c"]


def test_tag_missing_key():
    cache = LRUCache(2)
    assert cache.tag("ghost", "x") is False


def test_tag_no_duplicates():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.tag("a", "x")
    cache.tag("a", "x")
    assert cache.tags_for("a") == ["x"]


def test_new_entries_start_without_tags():
    cache = LRUCache(4)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.tag("a", "x")
    assert cache.tags_for("b") == []
    cache.put("c", 3)
    assert cache.tags_for("c") == []


def test_cache_entry_default_tags_independent():
    entries = [CacheEntry(i, i) for i in range(3)]
    entries[0].add_tag("x")
    assert entries[1].tags == []
    assert entries[2].tags == []


def test_put_copies_tags_list():
    cache = LRUCache(2)
    tags = ["x"]
    cache.put("a", 1, tags)
    tags.append("y")
    assert cache.tags_for("a") == ["x"]


def test_invalidate_multiple_entries():
    cache = LRUCache(5)
    for i in range(4):
        cache.put(i, i)
    for i in range(3):
        cache.tag(i, "x")
    cache.tag(3, "y")
    assert cache.invalidate_tag("x") == 3
    assert cache.keys() == [3]
    assert cache.invalidate_tag("x") == 0


def test_clear():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.clear()
    assert len(cache) == 0


def test_hit_rate_zero_when_unused():
    assert LRUCache(2).hit_rate == 0.0


def test_matches_reference_lru_model():
    rng = random.Random(0)
    cache = LRUCache(5)
    model = OrderedDict()
    for _ in range(3000):
        key = rng.randrange(10)
        if rng.random() < 0.5:
            expected = model.get(key)
            if key in model:
                model.move_to_end(key)
            assert cache.get(key) == expected
        else:
            val = rng.randrange(1000)
            model[key] = val
            model.move_to_end(key)
            while len(model) > 5:
                model.popitem(last=False)
            cache.put(key, val)
        assert cache.keys() == list(model)


def test_service_update_keeps_other_categories_cached():
    service = make_service()
    for pid in (1, 3, 5):
        service.get_product(pid)
    service.list_category("kitchen")
    loads = service.loads
    removed = service.update_price(1, 100)
    assert removed == 1
    service.get_product(3)
    service.get_product(5)
    service.list_category("kitchen")
    assert service.loads == loads


def test_service_update_refreshes_category_listing():
    service = make_service()
    first = service.list_category("books")
    assert first[0].price_cents == 1999
    service.update_price(1, 500)
    second = service.list_category("books")
    assert second[0].price_cents == 500


def test_service_update_validation():
    service = make_service()
    for bad in (lambda: service.update_price(1, -1), lambda: service.update_price(99, 10)):
        try:
            bad()
        except (ValueError, ProductNotFound):
            continue
        assert False, "expected an error"


def test_service_listing_is_copy():
    service = make_service()
    listing = service.list_category("books")
    listing.clear()
    assert len(service.list_category("books")) == 2


def test_format_price():
    assert format_price(5) == "0.05 EUR"
    assert format_price(1250) == "12.50 EUR"
    assert format_price(100, "USD") == "1.00 USD"


def test_service_many_requests_perform():
    products = [Product(i, f"P{i}", f"c{i % 5}", 100 + i) for i in range(500)]
    service = CatalogService(products, LRUCache(50))
    rng = random.Random(0)
    start = time.perf_counter()
    for _ in range(20000):
        service.get_product(rng.randrange(500))
    assert time.perf_counter() - start < 1.0
