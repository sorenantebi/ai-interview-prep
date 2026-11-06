"""Catalogue service: reads products through the cache."""

from catalog.cache import LRUCache
from catalog.utils import format_price


class ProductNotFound(KeyError):
    """Raised when a product id is unknown to the backend."""


class CatalogService:
    """Serves products and category listings, caching backend reads."""

    def __init__(self, products, cache=None):
        self._products = {p.id: p for p in products}
        self.cache = cache if cache is not None else LRUCache(64)
        self.loads = 0

    def get_product(self, product_id):
        key = f"product:{product_id}"
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        product = self._products.get(product_id)
        if product is None:
            raise ProductNotFound(product_id)
        self.loads += 1
        self.cache.put(key, product)
        self.cache.tag(key, f"category:{product.category}")
        return product

    def list_category(self, category):
        """Return the products of ``category`` sorted by name."""
        key = f"category:{category}"
        cached = self.cache.get(key)
        if cached is not None:
            return list(cached)
        result = sorted(
            (p for p in self._products.values() if p.category == category),
            key=lambda p: p.name,
        )
        self.loads += 1
        self.cache.put(key, result)
        self.cache.tag(key, key)
        return list(result)

    def update_price(self, product_id, price_cents):
        """Change a price and drop cached data of the product's category."""
        if price_cents < 0:
            raise ValueError("price must not be negative")
        product = self._products.get(product_id)
        if product is None:
            raise ProductNotFound(product_id)
        product.price_cents = price_cents
        return self.cache.invalidate_tag(f"category:{product.category}")

    def describe(self, product_id):
        product = self.get_product(product_id)
        return f"{product.name}: {format_price(product.price_cents)}"
