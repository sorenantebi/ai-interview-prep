"""The pricing service: turns a SKU, quantity and currency into a quote."""

from datetime import date

from pricing.discounts import apply_discounts
from pricing.models import Quote
from pricing.utils import percent_off


class PricingService:
    """Prices line items using a catalog, a sale schedule and a coupon book."""

    def __init__(self, catalog, sales, coupons, clock=date.today):
        self.catalog = catalog
        self.sales = sales
        self.coupons = coupons
        self._clock = clock

    def quote(self, sku, quantity, currency="USD", coupon_code=None, on=None):
        """Price ``quantity`` units of ``sku``.

        ``on`` is the date used to find running sales (default: today).
        """
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        if on is None:
            on = self._clock()
        currency = currency.strip().upper()

        list_unit = self.catalog.get_price(sku, currency)
        sale = self.sales.active_sale(sku, on)
        unit = list_unit
        if sale is not None:
            unit = percent_off(list_unit, sale.percent)
        subtotal = unit * quantity
        sale_name = sale.name if sale is not None else None

        if coupon_code is None:
            return Quote(
                sku=sku,
                currency=currency,
                quantity=quantity,
                list_unit_price=list_unit,
                sale_unit_price=unit,
                total=subtotal,
                sale_name=sale_name,
            )

        coupon = self.coupons.get(coupon_code)
        total = apply_discounts(subtotal, sale=sale, coupon=coupon)
        return Quote(
            sku=sku,
            currency=currency,
            quantity=quantity,
            list_unit_price=list_unit,
            sale_unit_price=unit,
            total=total,
            sale_name=sale_name,
            coupon_code=coupon.code,
        )

    def cart_total(self, items, currency="USD", coupon_code=None, on=None):
        """Sum the quote totals of ``items``, a list of ``(sku, quantity)``."""
        return sum(
            self.quote(sku, quantity, currency, coupon_code, on).total
            for sku, quantity in items
        )
