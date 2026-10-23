---
topic: "Location & Marketplace"
difficulty: Medium
problem: "Online Auction"
---
# Design an Online Auction (eBay-style) – Solution

**Topic:** Location & Marketplace · **Difficulty:** Medium · **Question:** Online Auction - Question

## 1. Requirements

**Functional**
- Seller creates an auction (item, starting price, end time)
- Buyer places a bid that must exceed the current highest bid (by a minimum increment)
- Viewers see the current price and bid count update in near real time
- When time expires the highest bid wins; winner and seller are notified

**Non-functional**
- **Strong consistency for bids:** exactly one highest bid, no lost or accepted-but-invalid bids
- Fast bid acknowledgement (< 200 ms); price updates to viewers within ~1 s
- Highly available reads; durable bid history (it is an audit trail)
- Exact, once-only closing even with crashes and multiple servers

**Out of scope:** payment and shipping, search/browse, proxy bidding (extension), fraud detection.

## 2. Back-of-envelope

- 10M active auctions × ~1 KB ≈ 10 GB of auction rows, tiny. Bids: say 20M/day × ~100 B ≈ 2 GB/day, about 700 GB/year.
- Average bid rate ≈ 20M/86,400 ≈ **230/s**. Peaks cluster at auction ends, so plan for ~5-10K/s overall, but any **single** auction maxes out at a few hundred bids/s.
- This matters: write load is modest, but contention is concentrated on one row per auction. The design problem is correctness under contention, not raw throughput.
- Reads: viewers ≫ bidders (say 100:1), so ~1M page loads/min must come from cache, and price changes must be pushed.

## 3. Core entities and API

Entities: `Auction { id, sellerId, title, startPrice, currentPrice, highBidderId, version, endTime, status }`, `Bid { id, auctionId, bidderId, amount, createdAt, idempotencyKey }`, `User`.

```
POST /auctions              { title, startPrice, endTime }              -> { auctionId }
GET  /auctions/{id}                                                    -> auction + top bid
POST /auctions/{id}/bids    { amount, idempotencyKey }                 -> 201 accepted | 409 outbid/too low | 410 ended
WS   /auctions/{id}/stream                                             -> price events
```

The bidder id comes from the auth token. The server stamps the time. The client clock is never trusted.

## 4. High-level design

!Online Auction - Diagram.excalidraw

- **Bid path:** the Bid Service runs a single atomic conditional write on the auction row in Postgres and appends the bid. After commit it publishes the new price to a per-auction Redis Pub/Sub channel.
- **Read/live path:** page loads hit the Redis cache. The WebSocket Gateway holds viewer connections and subscribes to the channels of the auctions they watch, pushing updates down.
- **Async:** an outbox row becomes a Kafka event, consumed by the Notifier (outbid emails/push, winner notice) and analytics.
- **Closing:** a scheduler (Auction Closer) finds auctions whose `endTime` passed and finalises them.

## 5. Deep dives

### 5.1 Accepting a bid correctly

The invariant: a bid is accepted only if it is higher than the current price *at the moment of commit* and the auction is still open.

| Approach | Mechanism | Pros | Cons |
|---|---|---|---|
| Read then write in app | check-then-act | Simple | Race: two bids both pass the check |
| `SELECT ... FOR UPDATE` | Pessimistic lock on the auction row | Correct | Holds locks across round trips; queues under contention |
| **Conditional UPDATE (atomic CAS)** | One statement checks and writes | Correct, short lock, no round trip | Losers get 0 rows and must report rejection |
| Optimistic `version` column | `WHERE version = :v` | Correct | Needless retries when the price actually allows the bid |
| Single writer per auction (Kafka partition by `auctionId`) | Serialise all bids for an auction in one consumer | Natural total order, huge throughput | Bid ack becomes async, more moving parts |
| Redis Lua script as source of truth | Atomic in-memory compare-and-set | Very fast | Durability and DB sync are risky; keep as accelerator only |

**Recommended:** conditional update in one transaction:

```sql
BEGIN;
UPDATE auctions
   SET current_price = :amt, high_bidder_id = :user, bid_count = bid_count + 1
 WHERE id = :id AND status = 'OPEN' AND end_time > now()
   AND :amt >= current_price + min_increment;      -- rows affected must be 1
INSERT INTO bids (auction_id, bidder_id, amount, idempotency_key, created_at) VALUES (...);
INSERT INTO outbox (...);
COMMIT;
```

- Zero rows updated: respond 409 (outbid or too low) or 410 (closed). Equal simultaneous bids are resolved by whichever transaction commits first; the other sees the new price and fails. Ties by commit order are the fair rule, using the **server** time.
- Use `now()` from the DB for the end-time check so all app servers share one clock.
- **Idempotency:** unique `(auction_id, idempotency_key)`. A retried request returns the original result rather than a second bid.
- The auction row is the single serialisation point. Per-auction throughput of hundreds of bids/s is fine for one Postgres row. Shard auctions across DBs by `auctionId`, so one auction never needs a cross-shard transaction.

### 5.2 Real-time price updates

- Polling every second from 100K viewers = 100K req/s for no information. Use **WebSocket** (or SSE, simpler and one-way, enough for price ticks).
- Flow: after commit, Bid Service publishes `{auctionId, price, bidCount}` to Redis channel `auction:{id}`. Each gateway node subscribes only to channels with local viewers and forwards messages.
- For hot auctions, **coalesce**: send at most one update every 100-250 ms with the latest price. Viewers do not need every intermediate bid, and this bounds fan-out cost.
- Pub/Sub is fire-and-forget. A reconnecting client re-fetches the current state (`GET /auctions/{id}`) and resumes, so lost messages only cause brief staleness. The DB is the truth.
- Scale gateways horizontally behind a layer-4 LB. If one channel has too many subscribers for a single Redis node, add a second fan-out tier (gateways subscribe to Redis, Redis shards by auction).

### 5.3 Closing auctions on time, exactly once

| Approach | How | Notes |
|---|---|---|
| Cron scanning the table | `WHERE status='OPEN' AND end_time <= now()` every second, using an index on `(status, end_time)` | Simple and robust; use `FOR UPDATE SKIP LOCKED` so several workers share the work |
| Per-auction timer in memory | `setTimeout` | Lost on restart, not distributed |
| Delayed queue / Redis sorted set (score = end time) | Workers pop due items | Fast, but needs reconciliation with the DB |
| Workflow engine timers (Temporal) | Durable timer per auction | Reliable, heavier |

**Recommended:** the DB scan with `SKIP LOCKED` as the source of truth, optionally prefaced by a Redis sorted set for sub-second precision. Closing is `UPDATE auctions SET status='CLOSED' WHERE id=:id AND status='OPEN' AND end_time <= now()`. This is idempotent: a second worker affects 0 rows. The winner is `high_bidder_id` on the row. Publish `AuctionClosed` via the outbox; the payment flow and notifications hang off that event.
- **Bid after close** is rejected because the bid's own `end_time > now()` predicate runs in the same row-level check, so there is no gap between "last accepted bid" and "closed".
- **Anti-sniping (optional):** if a bid lands within the last 2 minutes, extend `end_time` in the same update. The scanner reads the up-to-date `end_time`.

### 5.4 Hot auctions and read scaling

- Cache `auction:{id}` in Redis (price, bidCount, endTime); the bid path updates it after commit, with a short TTL as a fallback. Serve the page for all viewers from cache or the CDN plus WebSocket for live deltas.
- A flash auction with 10K bidders gives hundreds of conflicting conditional updates per second on one row; most lose fast. Rate-limit per user, and reject obviously low bids **before** hitting the DB using the cached current price (cheap pre-check, DB remains the judge).
- Bid history: append-only `bids` table, partitioned by time, indexed `(auction_id, created_at)`. Only the top few bids are public.

### 5.5 Failure modes

- **Crash after commit, before publish:** the outbox guarantees the event is still delivered by the relay; the live price may be late but eventually correct.
- **Crash before commit:** nothing accepted, the client retries with the same idempotency key.
- **DB failover:** synchronous replica promotion keeps accepted bids. Accept a short outage on writes rather than risk lost bids.
- **Notifier duplicates:** consumers dedupe by event id.

## 6. What interviewers look for

- **Junior:** entities, APIs, bids table, checks that a bid is higher.
- **Mid:** race condition awareness, atomic conditional update or locking, WebSocket for live price, scheduled closing.
- **Senior:** compare locking strategies and single-writer designs, idempotency, outbox, SKIP LOCKED closer, coalesced fan-out, hot-auction handling, failure semantics and server-side time.

## 7. Common pitfalls

- Check-then-act on the current price (lost update)
- Trusting the client clock or letting each app server decide "now"
- Polling for price updates
- A timer in app memory as the only closing mechanism
- Treating Redis or Pub/Sub as the source of truth for the winning bid
- No idempotency key, so retries create duplicate bids
