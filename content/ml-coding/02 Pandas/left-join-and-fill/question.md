---
topic: "Pandas"
difficulty: Medium
---
# Left Join and Fill

**Topic:** Pandas · **Difficulty:** Medium

## Problem

You get two DataFrames:

- `orders` with columns `order_id`, `customer_id` and `amount`;
- `customers` with columns `customer_id`, `name` and `country`. Each `customer_id` appears at most once here.

Return every order, in the same order as `orders`, with the customer's `name` and `country` added as the last two columns (`order_id`, `customer_id`, `amount`, `name`, `country`). Orders whose customer isn't in `customers` get `"unknown"` for both name and country. Use a default `0..n-1` index.

## Examples

**Example 1**
```text
Input: orders = {"order_id": [1, 2, 3], "customer_id": [10, 99, 10], "amount": [5.0, 7.5, 2.0]}, customers = {"customer_id": [10, 11], "name": ["ana", "ben"], "country": ["DE", "FR"]}
Output: {"order_id":[1,2,3],"customer_id":[10,99,10],"amount":[5.00000,7.50000,2.00000],"name":["ana","unknown","ana"],"country":["DE","unknown","DE"]}
Explanation: customer 99 isn't known, so order 2 gets "unknown".
```

**Example 2**
```text
Input: orders = {"order_id": [4], "customer_id": [11], "amount": [1.0]}, customers = {"customer_id": [11], "name": ["ben"], "country": ["FR"]}
Output: {"order_id":[4],"customer_id":[11],"amount":[1.00000],"name":["ben"],"country":["FR"]}
```

## Constraints

- `0 <= len(orders), len(customers) <= 10^5`
- `customer_id` is unique in `customers`
