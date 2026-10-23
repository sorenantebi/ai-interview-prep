---
topic: "Location & Marketplace"
difficulty: Medium
problem: "Local Delivery Service"
---
# Design a Local Delivery Service (Gopuff-style Instant Delivery) – Solution

**Topic:** Location & Marketplace · **Difficulty:** Medium · **Question:** Local Delivery Service - Question

## 1. Requirements

**Functional**
- Query availability: given a location, see the items that can be delivered within about an hour, as the **union of stock across nearby DCs**
- Place an order for several items at once

**Non-functional**
- Availability queries: fast (< 100 ms) and highly available, **eventual consistency is acceptable**
- Ordering: **strongly consistent**, no double-booking of the last unit
- Scale: ~10K DCs, ~100K items, ~10M orders/day, browse traffic far above order traffic
- Orders are never lost; order placement and dispatch are idempotent

**Out of scope:** payments, driver routing and live tracking, search/catalog APIs (keyword search is an extension), cancellations, substitutions and promotions, privacy/security, disaster recovery.

## 2. Back-of-envelope

- Orders: 10M/day ≈ 115/s average, ~500/s at dinner peak. A single Postgres primary can do several thousand small transactions/s, but a multi-item order touches several rows, so plan for sharding by region later.
- Availability reads: if each purchase takes ~10 searches and ~5% of sessions convert, 10M × 10 / 0.05 = 2B/day ≈ **~20K/s average**, 50K/s at peak (~100x orders). This must be served from cache/replicas, not the primary.
- Inventory table: 10K DCs × 100K SKUs = 1B possible rows, but each DC stocks a subset, say 5K SKUs, giving ~50M rows × ~50 B ≈ **2.5 GB**. It fits in RAM, so Redis can hold all of it.
- Orders: 10M/day × ~500 B (order + lines) ≈ 5 GB/day, ~1.8 TB/year, which is fine in Postgres with date partitioning and archiving.

## 3. Core entities and API

Entities: `Item { id, name, description, sku }` (the product type), `DistributionCenter { id, lat, long, zipcode, regionId }`, `Inventory { id, dcId, itemId, quantity, status }` (stock of an item at one DC), `Order { id, userId, status, createdAt }`, `OrderItem { id, orderId, inventoryId, quantity }`.

```
GET  /availability?lat={lat}&long={long}&items=[A,B,C]&page=1   -> { items: [ { itemId, quantity } ] }
POST /orders?lat={lat}&long={long}   { items: [{itemId, qty}] }  -> { orderId, status }
```

Send an idempotency key (header) on `POST /orders` so client retries do not create duplicate orders. `regionId` is a coarse area (for example the first 3 digits of the zip code) used later to partition inventory.

Availability is a **single aggregated view over all DCs near the address**. The client never needs to know which DC holds what. Inventory can be modelled either as one row per physical unit with a status, or as a quantity counter per (DC, item); we use the counter, which keeps the table small and the update a single conditional statement.

## 4. High-level design

!Local Delivery Service - Diagram.excalidraw

- **Availability:** the Availability Service asks the Nearby Service which DCs can serve the location (DC list synced into memory every few minutes), then reads stock for those DCs from Redis (or a read replica on a miss) and merges them into one item list.
- **Orders:** the Orders Service runs one SQL transaction on the inventory primary that decrements stock and inserts the order, then publishes an event (outbox) for dispatch.
- Postgres is the source of truth; Redis and read replicas are derived and slightly stale by design.

## 5. Deep dives

### 5.1 Which DCs can deliver to an address?

Delivery promise = real driving time within the window (about an hour, minus pick/pack time), not straight-line distance.

| Approach | How | Verdict | Pros / Cons |
|---|---|---|---|
| Straight-line radius | SQL/Haversine distance to each DC | Bad | Cheap, but ignores rivers, highways, traffic |
| Ask the travel-time API about every DC | Sync all DCs into memory, call Maps for each on every request | Bad | Accurate, but 10K calls per request: slow, expensive, impossible at ~20K requests/s |
| **Pruned candidate set** | Keep DCs in memory (refreshed every ~5 min), drop everything outside a max-optimistic radius (~60 miles for a 1-hour drive), call the travel-time API only for the few remaining candidates | **Great** | Cuts external calls by orders of magnitude; still one API fan-out per request |
| Precomputed service areas (extension) | Offline job maps geo cells (H3 or geohash) to `[dcId, etaMin]`, refreshed daily or when DCs/traffic patterns change | Great at very high QPS | O(1) in-memory lookup, no live API on browse; coarse at cell borders and stale vs. live traffic |

**Recommended:** prune by radius, then ask the travel-time service about the surviving candidates (a short-TTL cache keyed by cell and DC absorbs repeats). If browse traffic makes even that too chatty, move to precomputed cell-to-DC maps (only 10K DCs and a few hundred thousand cells, so the map fits in each service's memory) and use a live API only for the final checkout ETA, where the call volume is orders, not browses.

### 5.2 Fast availability reads

At ~20K queries/s (50K/s peak) the primary database cannot serve availability directly.

| Approach | Verdict | Trade-offs |
|---|---|---|
| Query the primary for every request | Bad | Read load collides with order writes |
| Redis cache of inventory results with a short TTL (~1 min) | Good | Fast hits; must invalidate or tolerate staleness on every inventory update |
| **Postgres read replicas, inventory partitioned by region** | **Great** | Partition by `regionId` (e.g. zip prefix) so a query touches one small partition; reads go to replicas (staleness acceptable), writes to the primary (strong consistency); cuts query load ~90% through region isolation |

Our design layers both: replicas partitioned by region as the base, with Redis in front for the hottest lookups, as described below.

- Query = `(DC list) × (items)`. Keep `stock:{dcId}` as a Redis hash `itemId → qty`, or a key per `(dcId, itemId)`. Fetch the 1-5 DCs in parallel (pipelined `HMGET`) and take `item in stock if any DC has qty > 0`.
- Updates reach Redis via the order transaction's event (outbox → Kafka → cache updater) and via restock events from DC systems. Entries can lag by seconds. That is acceptable because the order step re-checks authoritatively.
- Keyword search is out of scope; as an extension, Elasticsearch over the catalogue (item names), then filter by availability from the cache. Do not put stock inside the search index since it churns constantly.
- Shape the response to the user's region and mark low stock ("only 2 left") to reduce disappointment from stale reads.

### 5.3 Placing an order without overselling

All stock changes for an order live in one DB transaction:

```sql
BEGIN;
-- one conditional decrement per line, in a fixed itemId order (avoids deadlocks)
UPDATE inventory SET quantity = quantity - :qty
 WHERE dc_id = :dc AND item_id = :item AND quantity >= :qty;   -- check rows affected = 1
INSERT INTO orders (...);  INSERT INTO order_lines (...);
COMMIT;
```

If any decrement affects 0 rows, roll back and return "item unavailable". Compare options:

| Option | Mechanism | Verdict |
|---|---|---|
| Read stock, then write in app | check-then-act | Race condition: two buyers both see 1 |
| `SELECT ... FOR UPDATE` then update | Pessimistic row lock | Correct, but holds locks longer |
| **Conditional `UPDATE ... WHERE quantity >= qty`** | Atomic in one statement, optimistic | Correct, short lock, simple |
| Redis `DECRBY` as source of truth | Fast | Risky: durability and cross-store atomicity; use only as cache |
| Two-phase commit across DBs | When stock and orders are on different shards | Heavy; avoid by co-locating |

**Single-DC fulfilment** keeps the transaction on one shard: pick one DC (nearest with all items, else a smart split), and shard inventory and orders **by `dcId`/region** so the whole transaction is local. If an order must span DCs on different shards, use a saga: reserve stock at each DC with a TTL'd reservation, then confirm or release. Put an **idempotency key** on `POST /orders` (unique constraint) so retries do not double-charge.

### 5.4 Reservation, payment and dispatch

- Reserve stock at order creation (`status = PLACED`), then charge. If payment fails, run a compensating action (increment stock back). Alternatively, authorise payment first and capture on pickup.
- Publish `OrderPlaced` through an outbox table written in the same transaction, then relay to Kafka. Dispatch Worker consumes it, picks a driver near that DC, and tracks assignments. Consumers are idempotent by `orderId`.
- Reservations that never complete (user abandoned checkout) expire via a timer so held stock returns.

### 5.5 Scaling and failure modes

- **Read scale:** Redis plus replicas serve 50K/s. Cache the response per `(cell, category)` for a few seconds on top.
- **Write scale:** shard inventory/orders by DC region. Hot items (a viral snack) only contend on rows inside one DC, so conditional updates stay quick; for extreme contention, split the quantity into N sub-counters.
- **Redis stale or down:** fall back to a read replica; a stale "in stock" is caught at order time with a clear error.
- **DC goes offline:** a flag on the DC removes it from the cell map and from availability immediately.
- **Restock/count mismatch:** periodic reconciliation between the DC's physical counts and the DB; keep a safety buffer (don't expose the last 1-2 units).

## 6. What interviewers look for

- **Mid-level:** define the APIs and data model, deliver both the availability and the order path, and justify why a distance-only or per-request-travel-API approach fails. Understands each component; the interviewer may push on scale.
- **Senior:** moves quickly through the basics and optimises: prunes the DC candidate set, spots the availability read volume as the bottleneck (replicas, regional partitions, cache), distinct consistency per path, atomic order transaction with conditional update vs locking trade-offs.
- **Staff+:** deep in two or three areas and anticipates problems on their own: sharding by DC/region and a cross-shard saga, outbox, reservation expiry, hot-item contention (sub-counters), cache invalidation vs. TTL staleness, reconciliation with physical counts, precomputed service areas.

## 7. Common pitfalls

- Calling a maps API on every browse request
- Check-then-act on inventory without a transaction or conditional update
- Treating the Redis stock count as the source of truth
- Inconsistent lock ordering for multi-item orders, causing deadlocks
- Distributed transactions (2PC) when a smart shard key avoids them
- Putting live stock inside the search index
