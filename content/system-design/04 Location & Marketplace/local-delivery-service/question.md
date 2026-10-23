---
topic: "Location & Marketplace"
difficulty: Medium
problem: "Local Delivery Service"
---
# Design a Local Delivery Service (Gopuff-style Instant Delivery)

**Topic:** Location & Marketplace · **Difficulty:** Medium · **Answer:** Local Delivery Service - Solution

## Prompt

Design an on-demand local delivery service that sells convenience goods (snacks, drinks, household items) from its own network of small warehouses ("distribution centers", DCs) and delivers within about an hour. A customer enters a delivery address, sees only the items that can be delivered fast from nearby DCs, and places an order for several items.

## Requirements to pin down (ask the interviewer)

- Does the company own the DCs and stock (single inventory owner) or is it a marketplace of independent stores?
- Can one order be split across several DCs, or must a single DC fulfil all items?
- Is driver dispatch and live tracking, payments, search or cancellation in scope, or only availability and ordering?
- How strict is stock accuracy: is it acceptable to cancel an order occasionally?

## Scale hints

- ~10K DCs, ~100K distinct items (SKUs), ~10M orders/day
- Browsing is far more frequent than ordering (tens of thousands of availability queries per second)
- Availability results should load in < 100 ms
- Never sell stock that does not exist, even under concurrent orders for the last unit

## Think about before opening the answer

1. What are the entities, and which APIs are read-heavy vs write-heavy?
2. How do you decide which DCs can deliver to a given address, given traffic and geography rather than straight-line distance?
3. How do you compute "available items near me" quickly across several DCs?
4. How do two customers ordering the last item at the same time get handled?
5. Which data can be stale for a few seconds and which cannot?
6. How does the design change if inventory must be sharded across many databases?

## Self-check

- [ ] I can separate the read path (availability) from the write path (orders) and justify different consistency for each
- [ ] I can explain a transaction that decrements inventory and creates the order atomically
- [ ] I can estimate QPS for browse vs order traffic
- [ ] I can describe caching and its invalidation for inventory
