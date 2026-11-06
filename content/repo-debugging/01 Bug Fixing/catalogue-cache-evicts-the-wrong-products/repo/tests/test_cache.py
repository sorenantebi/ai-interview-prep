from catalog.cache import LRUCache
from catalog.models import CacheEntry


def test_put_and_get():
    cache = LRUCache(2)
    cache.put("a", 1)
    assert cache.get("a") == 1


def test_miss_returns_default():
    cache = LRUCache(2)
    assert cache.get("nope") is None
    assert cache.get("nope", 7) == 7


def test_evicts_oldest_when_full():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert "a" not in cache
    assert cache.keys() == ["b", "c"]


def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)
    assert "a" in cache, "recently read entry must survive eviction"
    assert "b" not in cache


def test_contains_does_not_refresh():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert "a" in cache
    cache.put("c", 3)
    assert "a" not in cache


def test_tags_are_per_entry():
    cache = LRUCache(4)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.tag("a", "x")
    assert cache.invalidate_tag("x") == 1
    assert "a" not in cache
    assert "b" in cache


def test_cache_entries_do_not_share_default_tags():
    first = CacheEntry("k1", 1)
    first.add_tag("x")
    second = CacheEntry("k2", 2)
    assert second.tags == []


def test_hit_rate():
    cache = LRUCache(2)
    cache.get("a")
    cache.put("a", 1)
    cache.get("a")
    assert cache.hit_rate == 0.5
