"""Per-category tax rates."""

from cart.utils import round_div

DEFAULT_RATES_BP = {"standard": 1900, "food": 700, "book": 700}


class TaxTable:
    """Maps a product category to a tax rate in basis points (1/100 of a percent)."""

    def __init__(self, rates_bp=None, default_bp=1900):
        self._rates = dict(DEFAULT_RATES_BP if rates_bp is None else rates_bp)
        self._default = default_bp

    def rate_bp(self, category: str) -> int:
        return self._rates.get(category, self._default)

    def tax_for(self, category: str, net_cents: int) -> int:
        """Tax on ``net_cents`` for the category, rounded half up to a cent."""
        return round_div(net_cents * self.rate_bp(category), 10000)
