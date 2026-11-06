# Catalogue cache evicts the wrong products - Solution

## Root causes / approach
**1. `catalog/cache.py`, `LRUCache.get`:** a hit returned the value but never moved the key to the end of the `OrderedDict`. The order therefore reflected insertion order only, so the cache behaved like a FIFO. Busy products were evicted as soon as they were old enough. Fix: call `self._entries.move_to_end(key)` on a hit. Misses and `__contains__` / `__len__` must not touch the order, which the tests check.

**2. `catalog/models.py`, `CacheEntry.__init__`:** `tags=[]` is a mutable default argument, evaluated once. Every entry created without explicit tags stored the very same list object, so `add_tag` on one entry tagged all of them. `invalidate_tag("category:books")` then removed every entry in the cache, including unrelated categories. Fix: default to `None` and give each entry its own list (`list(tags) if tags is not None else []`). Copying a passed list also stops callers from mutating an entry's tags afterwards.

## How to find it
- Start with `test_get_refreshes_recency` in `tests/test_cache.py`. It is a minimal two-key scenario that points straight at `LRUCache.get`; compare it with `put`, which does reorder.
- `test_tags_are_per_entry` and `test_cache_entries_do_not_share_default_tags` fail at the cache and model level. Printing `cache.tags_for("b")` after tagging only `"a"` shows the tag leaking, and the `CacheEntry` constructor with its `tags=[]` default is the cause.
- `test_update_price_only_invalidates_own_category` in `tests/test_service.py` is the same bug seen from the service layer. Once the two root causes are fixed, all visible and hidden tests pass.
