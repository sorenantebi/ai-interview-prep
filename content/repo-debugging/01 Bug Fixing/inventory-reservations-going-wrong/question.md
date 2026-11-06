---
difficulty: Easy
kind: bug-fix
---
# Inventory Reservations Going Wrong

**Kind:** Bug fix · **Difficulty:** Easy

## Scenario
The warehouse team uses a small inventory service to track stock per product and to reserve units while an order is being packed. Support has two complaints. Orders are still being accepted for products that have exactly zero units left, and after a delivery is restocked, the units that were reserved for open orders vanish from the books. The picking list for low-stock products also shows the wrong item first.

## Your tasks
1. Orders go through for products with nothing left to sell. Find and fix the cause (the failing tests show the symptoms).
2. Restocking a product loses track of units that are currently reserved. Find and fix the cause.
3. The low-stock report is not ordered the way the picking team expects. Find and fix the cause.
4. Make sure all visible tests pass and think about which edge cases the hidden tests might cover.

## Notes
- The entry point is `InventoryService` in `inventory/service.py`; the report helpers live in `inventory/reports.py`.
- "Available" means units on hand minus units reserved. Quantities are always positive integers.
- Each bug is in a different file. Do not change the public function signatures.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
