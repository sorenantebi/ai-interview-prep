# Wrong prices in the pricing service - Solution

## Root causes / approach

**Bug 1: stale cache key (`pricing/catalog.py`, `Catalog._cache_key`)**
`_cache_key(sku, currency)` accepted the currency but returned only the normalised SKU. The first lookup of a SKU in any currency filled the cache entry for that SKU, and every later lookup in another currency was served from it. That is why EUR prices showed up in USD answers (and the reverse), depending on which currency was requested first. The fix is to include the currency in the key: `return (sku.strip().upper(), currency.strip().upper())`. Caching is kept: one miss per distinct (SKU, currency) pair, and failed lookups are still not cached.

**Bug 2: sale applied twice (`pricing/service.py`, `PricingService.quote`)**
By the time the coupon is handled, `subtotal` is already built from `unit`, the sale-reduced unit price. The coupon branch then called `apply_discounts(subtotal, sale=sale, coupon=coupon)`, and `apply_discounts` applies the sale first, so the sale percentage was applied a second time. The bug only shows when a coupon and a sale are combined, because the sale-only path returns early and the coupon-only path has `sale=None`. For 1200 with a 20% sale and a 10% coupon: expected 960 -> 864, actual 960 -> 768 -> 691. The fix is `apply_discounts(subtotal, coupon=coupon)`. `apply_discounts` itself is correct when given an undiscounted amount, so it stays unchanged (hidden tests still call it directly).

## How to find it
1. Run the tests. Two groups fail: the cross-currency catalog tests (`test_usd_after_eur_lookup`, `test_eur_after_usd_lookup`, `test_mixed_currencies_on_one_service`) and `test_sale_and_coupon`.
2. For the first group, note that each test passes alone with a fresh catalog; only the second lookup of the same SKU is wrong. That points at the memoisation. Read `get_price` and `_cache_key`, and print `catalog._cache` after two lookups: there is one entry per SKU, not per (SKU, currency).
3. For the second group, note that sale-only and coupon-only tests pass and only the combination is wrong. Do the arithmetic by hand (1200 -> 960 -> 864) and compare with the 691 you get. 691 is 960 reduced by 20% and then by 10%, so the sale is applied twice. Follow the data in `quote`: `subtotal` is already sale-reduced, yet `apply_discounts` is given the sale again.
4. After both fixes, rerun the visible tests, then think about the edge cases the hidden tests probe: currency case and whitespace sharing one cache entry, failed lookups not being cached, and several sales or currencies on one service.
