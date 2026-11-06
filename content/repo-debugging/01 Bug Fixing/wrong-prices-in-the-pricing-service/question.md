---
difficulty: Medium
kind: bug-fix
---
# Wrong prices in the pricing service

**Kind:** Bug fix · **Difficulty:** Medium

## Scenario
The pricing service quotes unit and order prices in USD and EUR for the web shop. It looks up list prices from a catalog, applies any running sale, and then an optional coupon code. Since last week, customer support has been getting complaints. Some US customers are quoted prices that look like the EUR ones, and some orders that use a coupon during a sale come out cheaper than the advertised discount rules allow.

## Your tasks
1. Users report that the price shown for a currency sometimes depends on which currency was requested earlier. Find and fix the cause (the failing tests show the symptoms).
2. Finance reports that when a coupon is used on a product that is currently on sale, the customer gets more off than they should. Find and fix the cause.
3. Make sure the whole visible test suite passes without changing the public API of the package or removing the catalog's caching.

## Notes
- The entry point is `PricingService.quote()` in `pricing/service.py`. `cart_total()` sums quotes for several items.
- All amounts are integers in minor units (cents). A sale is applied first, then the coupon is applied to the already reduced price. Each percentage is applied once.
- Sales are inclusive of both their start and end dates.
- `Catalog.misses` counts lookups that were not served from the cache; tests rely on it, so keep the caching behaviour.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
