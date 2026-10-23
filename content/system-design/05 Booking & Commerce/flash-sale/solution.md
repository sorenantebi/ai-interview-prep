---
topic: "Booking & Commerce"
difficulty: Hard
problem: "Flash Sale"
---
# Design a Flash Sale System – Solution

**Topic:** Booking & Commerce · **Difficulty:** Hard · **Question:** Flash Sale - Question

## 1. Requirements

**Functional**
- Users see the product page and a countdown, then attempt to buy when the sale opens
- Each user can buy at most K units (usually 1); the system confirms or rejects quickly
- Winners get an order and pay within a time limit; unpaid stock returns to the pool

**Non-functional**
- **Never oversell** (hard invariant); never double-charge
- Survive ~1M req/s for a few seconds with p99 < 300 ms for the accept/reject decision
- Isolation: the spike must not take down the rest of the shop
- Fairness and bot resistance; graceful "sold out" experience

**Out of scope:** product catalog, shipping, refunds beyond the stock-return flow.

## 2. Back-of-envelope

- 10M users × ~3 clicks in the first 10 s ≈ 30M requests → **~3M/s peak** (assume we need 1M/s capacity after the waiting room and client-side throttling).
- Stock 10K: only **0.1%** of requests can succeed. Design the funnel so that ≥ 99.9% die at the edge or in memory.
- Successful orders: 10K in maybe 5 s = ~2K orders/s. Easy for Postgres if it is behind a queue; impossible if 1M/s of failed attempts also hit it.
- One Redis node does ~100K ops/s for simple commands; a single hot key can't be split, so the stock gate needs one hot-key design (see 5.2), not more nodes blindly.

## 3. Core entities and API

Entities: `Sale { id, productId, stock, startsAt, limitPerUser }`, `Order { id, saleId, userId, status: PENDING_PAYMENT|PAID|EXPIRED, qty }`.

```
GET  /sales/{id}                          -> static info + server-time offset (CDN-cached)
POST /sales/{id}/buy  (Idempotency-Key)   -> 202 { requestId }  or 409 SOLD_OUT / 429
GET  /orders/by-request/{requestId}       -> { status: PENDING|WON|LOST }
POST /orders/{id}/pay                     -> payment flow (within 10 min)
```

## 4. High-level design

!Flash Sale - Diagram.excalidraw

Think of it as a **funnel**; each layer removes most of the traffic:
1. **CDN** serves the static sale page, assets and the countdown (no origin hits before the start).
2. **Gateway** authenticates, rate limits per user/IP/device and checks a CAPTCHA/proof-of-work token for suspicious clients.
3. **Waiting room** (optional but valuable for huge audiences) admits a controlled number of users.
4. **Order Service (hot path)** is stateless and does one thing: run an atomic check in **Redis** (user not already bought, stock > 0, decrement). A "no" is returned in single-digit ms.
5. Winners are put on **Kafka**; **order workers** create the order in Postgres, handle payment and confirm. The user polls (or gets pushed) the outcome.

## 5. Deep dives

### 5.1 Why not decrement stock in the database

`UPDATE inventory SET stock = stock - 1 WHERE id = ? AND stock > 0` is correct, but it serializes on one row: roughly 1-5K updates/s with row locks, and the other 995K req/s would pile up on connections. Latency explodes and the DB takes the rest of the shop with it. So the **database is the system of record, not the gatekeeper**; the gate is in memory.

### 5.2 The in-memory stock gate (atomic)

Redis Lua script, executed atomically per request:

```
-- KEYS: stock:{sale}, buyers:{sale}   ARGV: userId
if redis.call('SISMEMBER', KEYS[2], ARGV[1]) == 1 then return -1 end  -- already bought
if tonumber(redis.call('GET', KEYS[1])) <= 0 then return 0 end         -- sold out
redis.call('DECR', KEYS[1]); redis.call('SADD', KEYS[2], ARGV[1]); return 1
```

- Single-threaded Redis makes this atomic; no oversell and no per-user duplicates.
- **Hot key problem:** all traffic hits one key. Options: (a) shard the stock into N sub-counters (e.g. 10 × 1,000 units), route a user to a shard by hash of userId, and fall back to other shards when empty; (b) a local in-process "sold-out" flag: after the first `0` the service short-circuits locally, so Redis only sees the first moments; (c) pre-filter with a **random lottery** (below) so only ~2x the stock reaches the gate.
- Sold-out is monotonic, so it is safe to cache "SOLD_OUT" in the gateway/CDN edge for a few seconds.

### 5.3 Reconciliation: Redis vs DB, and failures

!Flash Sale - Deep Dive Diagram.excalidraw

- Pre-load `stock` into Redis before the sale from the DB. Redis is the **fast gate**, the DB inventory is the **truth**. Workers decrement DB stock inside the order transaction with `WHERE stock > 0`; if that ever fails, the worker marks the order failed and refunds (a safety net, should be ~never).
- **Redis dies mid-sale:** the AOF/replica may lack the last few decrements, so recount: on failover, set `stock = DBStock - pendingReservations` and rely on the DB conditional update. Prefer to slightly **undersell** (hold back a small buffer, release it at the end) over overselling.
- **Reserved but unpaid:** an order is `PENDING_PAYMENT` with a 10-minute TTL. A delayed job (Kafka delay topic, Redis ZSET or DB scheduler) expires it, increments DB stock and Redis `stock` (`INCR`), and removes the user from `buyers` if retries are allowed. Released units go to the next users via a second small "release" wave.
- Workers are idempotent: key = `saleId:userId`, enforced by a **unique constraint** on the order table.

### 5.4 Idempotency and exactly-once effects

- Client sends an `Idempotency-Key` (or the server derives `saleId:userId`). The Lua gate's `buyers` set already rejects repeats; the unique constraint on orders protects against Kafka redelivery (at-least-once).
- Payment uses the order id as the provider's idempotency key, so a retried worker call never double charges.

### 5.5 Fairness, queueing and abuse

| Strategy | Effect | Trade-off |
|---|---|---|
| First-come-first-served | Simple | Rewards bots and best network; hot-key stampede |
| **Random lottery in a short window** (collect requests for 1-2 s, then pick winners) | Fair, flattens the spike | Slightly delayed answer |
| Waiting room with random positions + admission tokens | Smooth load | More moving parts |
| Pre-registration / verified accounts | Strong anti-bot | Extra product friction |

Plus: per-user and per-device limits, CAPTCHA or proof-of-work on the buy call, blocking disposable accounts, and server-signed tokens that tie a buy to a logged-in session.

### 5.6 Isolation and capacity

- Dedicated Redis, Kafka partitions and a separate cluster/namespace for the flash-sale hot path; autoscaling cannot react in seconds, so **pre-scale** before the event and load test.
- Shed load aggressively: return 429/"you're in the queue" rather than queuing in-process. Use static fallback responses at the CDN when the origin degrades.
- Kafka decouples the burst from Postgres: workers drain at a constant 2-5K orders/s; partition by `userId` or `saleId`.

## 6. What interviewers look for

- **Junior:** knows the DB row lock is the bottleneck, proposes a cache/queue, atomic decrement.
- **Mid:** layered funnel (CDN, rate limit, Redis gate), async order processing with Kafka, idempotency, unpaid reservation expiry.
- **Senior:** hot-key mitigation (sharded counters, local sold-out flag), Redis-failure recovery with undersell bias, reconciliation with DB as truth, fairness and bot defense, capacity pre-scaling and isolation.

## 7. Common pitfalls

- Sending every request to the database with `SELECT ... FOR UPDATE`
- Check-then-decrement as two Redis calls (race condition); must be one atomic script
- No story for abandoned reservations, so stock is lost forever
- Forgetting idempotency, resulting in double orders on retry or redelivery
- Auto-scaling as the main plan for a spike that lasts seconds
- Ignoring bots, so 99% of the stock goes to scripts
