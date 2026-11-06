---
difficulty: Medium
kind: extend
---
# Discount codes for the shopping cart

**Kind:** Extend the codebase · **Difficulty:** Medium

## Scenario
The `cart` package prices shopping carts for a small web shop: line items, per-category tax and a quote with subtotal, tax and total. Marketing wants discount codes at checkout: a percentage off, a fixed amount off, and buy-one-get-one-free on a single SKU. The classes and method signatures are already in place, but the discount logic itself is missing and pricing ignores any codes on a cart.

## Your tasks
1. Make discount codes work end to end: `CartService.apply_code(cart_id, code)` attaches a code to a cart, `CartService.remove_code(cart_id, code)` detaches it, and `CartService.quote(cart_id)` reflects the discounts. The tests in `tests/test_discounts.py` show the expected behaviour.
2. Follow these rules for the three kinds of code:
   - `PercentOff`: takes `percent` percent off every line. Each line's share is rounded half up to whole cents.
   - `FixedOff`: takes a fixed number of cents off the cart. It never exceeds what is left to pay, and it is spread across the lines in proportion to what each line costs at that point.
   - `BuyOneGetOne`: for the given SKU, every second unit is free (`quantity // 2` free units).
3. Follow these stacking rules:
   - A `BuyOneGetOne` code stacks with any other code. A cart can have at most one `BuyOneGetOne` per SKU.
   - A cart can have at most one cart-wide code (`PercentOff` or `FixedOff`), not one of each.
   - The same code cannot be applied twice.
   - A rejected code raises `DiscountError` and leaves the cart unchanged.
   - Buy-one-get-one is always applied first, then the cart-wide code works on the reduced amounts, regardless of the order the codes were applied in.
4. Tax is charged on what the customer actually pays, i.e. on each line after discounts.

## Notes
- All money is in integer cents. `cart/utils.py` already has helpers for rounding and for splitting an amount proportionally.
- Codes are case-insensitive and surrounding whitespace is ignored; an unknown code raises `DiscountError`.
- Unknown cart ids and SKUs raise `KeyError`.
- Existing tests pass today and must keep passing.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
