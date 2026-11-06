"""Product catalog with a memoised price lookup."""

from pricing.models import UnknownCurrency, UnknownProduct


class Catalog:
    """Holds products and answers price questions.

    Prices are looked up often and the product table is large in production,
    so successful lookups are cached.
    """

    def __init__(self, products):
        self._products = {}
        for product in products:
            self._products[product.sku.upper()] = product
        self._cache = {}
        self.misses = 0

    def _cache_key(self, sku, currency):
        """Normalise the arguments of a lookup into a cache key."""
        return sku.strip().upper()

    def get_price(self, sku, currency="USD"):
        """Return the list price of ``sku`` in ``currency`` (minor units)."""
        currency = currency.strip().upper()
        key = self._cache_key(sku, currency)
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        self.misses += 1
        product = self._products.get(sku.strip().upper())
        if product is None:
            raise UnknownProduct(sku)
        if currency not in product.prices:
            raise UnknownCurrency(currency)
        price = product.prices[currency]
        self._cache[key] = price
        return price

    def clear_cache(self):
        """Forget all cached prices, e.g. after the catalog was reloaded."""
        self._cache.clear()
