# Inventory Reservations Going Wrong - Solution

## Root causes / approach

**1. `inventory/service.py`, `InventoryService.reserve`: zero stock is never rejected.**
The guard was `if product.available > 0 and quantity > product.available`. The extra `available > 0` condition means the check is skipped entirely when nothing is left, so any quantity is accepted and `reserved` grows past `on_hand` (available goes negative). The fix is to drop that condition and use the plain check `if quantity > product.available`. This still allows reserving exactly the remaining units and rejects everything else, including requests against zero stock.

**2. `inventory/models.py`, `Product.restock`: reserved units are wiped.**
The method did `self.on_hand = self.available + quantity` and `self.reserved = 0`. It treated the delivery as if it started from the available count and then forgot the open reservations. `on_hand` therefore dropped by the reserved amount and `reserved` went to 0, so later `release` and `commit` calls on existing reservations drove the counters negative. The fix is `self.on_hand += quantity`; delivery only changes the physical stock, and `reserved` is left alone.

**3. `inventory/reports.py`, `low_stock`: wrong sort key.**
The list was sorted by `(p.on_hand, p.sku)`. A product with 100 units on hand of which 98 are reserved is more urgent than one with 4 untouched units, but it sorted last. The docstring says "fewest units available first", so the key must be `(p.available, p.sku)`.

## How to find it
- Start with `test_reserve_when_nothing_left_raises`. Reproduce it in a REPL: add a product with 2 units, reserve 2, then reserve 1 and print `product.available` (it is -1). That points straight to the guard in `reserve`; reading its condition shows the zero case is skipped.
- Next read `test_restock_keeps_reserved_units`. The assertion message says what is lost, and the only code that touches `reserved` during a restock is `Product.restock`, which `InventoryService.restock` delegates to. Printing `on_hand` and `reserved` before and after makes the faulty arithmetic obvious.
- For `test_low_stock_most_urgent_first`, print the `(sku, on_hand, available)` of the returned list. It is ordered by `on_hand`, while the docstring and test expect `available`. Check the `key=` of the `sorted` call.
- After the fixes, rerun all tests and think about neighbours of each bug: failed reservations must not change state, restock followed by release/commit, and ties in the report.
