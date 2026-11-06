"""Domain objects for the cart package."""

from dataclasses import dataclass, field

from cart.discounts import Discount


@dataclass(frozen=True)
class Product:
    """A sellable product. Prices are in cents."""

    sku: str
    name: str
    unit_price_cents: int
    category: str = "standard"


@dataclass
class LineItem:
    """A product and how many units of it are in a cart."""

    product: Product
    quantity: int

    @property
    def sku(self) -> str:
        return self.product.sku

    @property
    def unit_price_cents(self) -> int:
        return self.product.unit_price_cents

    @property
    def gross_cents(self) -> int:
        return self.product.unit_price_cents * self.quantity


@dataclass
class Cart:
    """Line items keyed by sku, plus the discount codes applied to them."""

    cart_id: int
    items: dict = field(default_factory=dict)
    discounts: list = field(default_factory=list)

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        line = self.items.get(product.sku)
        if line is None:
            self.items[product.sku] = LineItem(product, quantity)
        else:
            line.quantity += quantity

    def remove(self, sku: str) -> None:
        del self.items[sku]

    def lines(self) -> list:
        """Line items ordered by sku."""
        return [self.items[sku] for sku in sorted(self.items)]

    def add_discount(self, discount: Discount) -> None:
        """Attach a discount, enforcing the stacking rules.

        Raises ``DiscountError`` (and leaves the cart unchanged) if the code
        is already applied, if a cart-wide discount is already present, or if
        another buy-one-get-one on the same sku is already present.
        """
        raise NotImplementedError

    def remove_discount(self, code: str) -> None:
        """Detach the discount with this code; ``DiscountError`` if not applied."""
        raise NotImplementedError
