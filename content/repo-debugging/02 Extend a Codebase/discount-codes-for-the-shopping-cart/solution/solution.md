# Discount codes for the shopping cart - Solution

## Root causes / approach
The existing design already has the right seams, so the feature is built by filling them in rather than adding new structure.

- **`cart/discounts.py`**: each discount implements `amounts(lines, nets)`, returning `{sku: cents_to_deduct}`. Discounts never touch the cart, which keeps them easy to test and lets pricing compute tax afterwards on the net figures.
  - `PercentOff` uses the existing `round_div` per line (half up), as specified.
  - `FixedOff` caps the amount at `sum(nets)` and uses the existing `split_proportionally` helper over the lines sorted by sku, with the current net amounts as weights. That helper guarantees the shares add up exactly and also copes with an all-zero cart, so there is no special-casing.
  - `BuyOneGetOne` deducts `quantity // 2 * unit_price` for the matching line, or nothing if the sku is not in the cart.
  - `CART_WIDE = (PercentOff, FixedOff)` names the group that is mutually exclusive.
- **`cart/models.py`**: `Cart.add_discount` checks the three stacking rules (same code, second cart-wide code, second BOGO on the same sku) before appending, so a rejected code leaves the cart unchanged. `remove_discount` removes by normalised code or raises `DiscountError`.
- **`cart/pricing.py`**: `price_cart` keeps running `nets` per sku and applies the discounts in a stable order with line-level ones first (`sorted(..., key=isinstance(d, CART_WIDE))`). That is what makes "BOGO first, then the cart-wide code" independent of the order the codes were applied in. Tax is then computed on each line's net amount, and `build_quote` totals everything unchanged.
- **`cart/service.py`**: `apply_code` normalises the code with the existing `normalize_code`, looks it up in the catalogue built in `__init__` (unknown means `DiscountError`) and delegates to the cart. `remove_code` just delegates.

Complexity is linear in lines times discounts for each quote, and a cart has at most a handful of discounts.

## How to find it
Start with `tests/test_discounts.py` and run it: every test fails with `NotImplementedError`, and the tracebacks point at `CartService.apply_code`, then `Cart.add_discount`, then `Discount.amounts`. Read `cart/discounts.py` for the contract (`amounts` receives `lines` and `nets`), then `pricing.price_cart` to see where the amounts must be applied, noting that it currently sets `discount_cents` to 0 and taxes the gross. Next look at `cart/utils.py`, which already offers `round_div`, `split_proportionally` and `normalize_code`. Work in the order service, model, discounts, pricing, and hand-check the expected numbers in the tests (for example 10% of 3750 is 375, with tax of 410 + 85 on 2160 and 1215) before running again.
