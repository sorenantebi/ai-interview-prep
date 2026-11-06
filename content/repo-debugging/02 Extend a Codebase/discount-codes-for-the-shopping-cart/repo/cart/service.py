"""Entry point used by the web layer: carts are addressed by integer id."""

from cart.models import Cart
from cart.pricing import Quote, price_cart
from cart.tax import TaxTable
from cart.utils import normalize_code


class CartService:
    """Keeps carts in memory and prices them."""

    def __init__(self, products, tax_table=None, discounts=()):
        self._products = {p.sku: p for p in products}
        self._tax_table = tax_table or TaxTable()
        self._discounts = {normalize_code(d.code): d for d in discounts}
        self._carts = {}
        self._next_id = 1

    def create_cart(self) -> int:
        cart_id = self._next_id
        self._next_id += 1
        self._carts[cart_id] = Cart(cart_id)
        return cart_id

    def _cart(self, cart_id: int) -> Cart:
        return self._carts[cart_id]

    def add_item(self, cart_id: int, sku: str, quantity: int = 1) -> None:
        product = self._products[sku]
        self._cart(cart_id).add(product, quantity)

    def remove_item(self, cart_id: int, sku: str) -> None:
        self._cart(cart_id).remove(sku)

    def apply_code(self, cart_id: int, code: str) -> None:
        """Attach the discount registered under ``code`` to the cart."""
        raise NotImplementedError

    def remove_code(self, cart_id: int, code: str) -> None:
        """Detach a previously applied code from the cart."""
        raise NotImplementedError

    def quote(self, cart_id: int) -> Quote:
        return price_cart(self._cart(cart_id), self._tax_table)
