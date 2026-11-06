"""Sales, coupons and the rules for combining them."""

from pricing.models import UnknownCoupon
from pricing.utils import percent_off


class SaleSchedule:
    """A collection of sales that can be queried by SKU and date."""

    def __init__(self, sales=()):
        self._sales = list(sales)

    def add(self, sale):
        """Register another sale."""
        self._sales.append(sale)

    def active_sale(self, sku, on):
        """Return the best sale covering ``sku`` on date ``on``, or None.

        If several sales overlap, the one with the highest percentage wins.
        """
        wanted = sku.strip().upper()
        matches = [
            sale
            for sale in self._sales
            if wanted in sale.skus and sale.start <= on <= sale.end
        ]
        if not matches:
            return None
        return max(matches, key=lambda sale: sale.percent)


class CouponBook:
    """Looks coupons up by their (case-insensitive) code."""

    def __init__(self, coupons=()):
        self._coupons = {coupon.code.upper(): coupon for coupon in coupons}

    def get(self, code):
        """Return the coupon for ``code`` or raise ``UnknownCoupon``."""
        try:
            return self._coupons[code.strip().upper()]
        except KeyError:
            raise UnknownCoupon(code) from None


def apply_discounts(amount, sale=None, coupon=None):
    """Apply ``sale`` and then ``coupon`` (either may be None) to ``amount``.

    Each percentage is applied to the amount left by the previous step.
    """
    total = amount
    if sale is not None:
        total = percent_off(total, sale.percent)
    if coupon is not None:
        total = percent_off(total, coupon.percent)
    return total
